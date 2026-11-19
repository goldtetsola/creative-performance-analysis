#!/usr/bin/env python3
"""
Capture a video via Gemini in quick or detailed mode.

Quick captures visual events, speech and readable text. Detailed uses the
original spatial/audio analysis prompt. Prompts live beside this skill.

Usage:
    analyze_video.py <video-path> [output-path] [--mode quick|detailed]

If output-path is omitted, defaults to:
    <video-dir>/Analyses/<video-filename>.<mode>.md

Set GEMINI_API_KEY in the environment. No credentials are printed.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PROMPT_PATH = SCRIPT_DIR / "prompts" / "full.md"
QUICK_PROMPT_PATH = SCRIPT_DIR / "prompts" / "quick.md"
DEFAULT_MODEL = "gemini-2.5-flash"
sys.path.insert(0, str(SCRIPT_DIR))
import media_capture
sys.path.pop(0)

# This is the "Ad Substance Summary" deliverable that gets appended to the
# detailed system instruction. Prompted structure is not proof of fidelity.
SUBSTANCE_DELIVERABLE = """
After completing all required structured sections, ALSO append a final \
"## Ad Substance Summary" section containing:
- Full verbatim spoken transcript (numbered by speaker turn if multiple speakers, with timestamps)
- All on-screen text in chronological order with timestamps
- Observable presentation (talking head, demonstration, motion graphics, etc.); do not infer who produced it
- Length and apparent aspect ratio
- Hook: exact first 3 seconds described (visual + audio + on-screen text)
- Body: how the middle 70% builds
- Close: how it ends, including any CTA wording
- Any badges/stickers/offers superimposed
- The single most distinctive creative element
"""

SYSTEM_INSTRUCTION_PREAMBLE = """You are a meticulous video analyst. Your \
ENTIRE output must follow the structured analysis methodology below. \
Begin with the \
<mandatory_audio_verification> three passes and produce all three declarations \
verbatim. Then complete <temporal_visibility_tracking> with the full \
visibility log declaration. Then proceed through every numbered phase. Do not \
summarize prematurely or skip to conclusions. The caller requires the full \
structured analysis. Report any unavailable evidence or incomplete coverage \
honestly. Never claim a check passed merely because its declaration is \
requested; mark that check incomplete instead.
"""


def resolve_gemini_api_key() -> str:
    """Read the user's own key from the environment."""
    if key := os.environ.get("GEMINI_API_KEY", "").strip():
        return key
    raise SystemExit("Set GEMINI_API_KEY to your own Gemini API key.")


def needs_safe_filename(path: Path) -> bool:
    """
    Check if filename contains characters that break google-genai's upload
    (specifically: characters that httpx can't encode in ASCII headers).
    Emoji and many non-ASCII characters trigger this.
    """
    try:
        path.name.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True


def copy_to_safe_path(src: Path) -> Path:
    """
    Copy a file with unsafe filename to /tmp with a safe ASCII filename.
    Returns the new path. Caller is responsible for cleanup if desired.
    """
    suffix = src.suffix if src.suffix.isascii() else ".bin"
    fd, tmp_path = tempfile.mkstemp(suffix=suffix, prefix="gemini_upload_")
    os.close(fd)
    tmp = Path(tmp_path)
    try:
        shutil.copy2(src, tmp)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return tmp


def wait_for_active(client, upload, timeout_s: int = 240):
    """Poll an uploaded file until it's ACTIVE or FAILED."""
    started = time.monotonic()
    while True:
        if time.monotonic() - started > timeout_s:
            raise SystemExit(f"Gemini upload timeout (>{timeout_s}s)")
        try:
            current = client.files.get(name=upload.name)
        except Exception:
            current = upload
        state = str(getattr(current, "state", "")).upper()
        if "ACTIVE" in state:
            return current
        if "FAILED" in state:
            raise SystemExit("Gemini upload state = FAILED")
        time.sleep(2)


def analyze(
    video_path: Path,
    output_path: Path,
    prompt_path: Path,
    model: str,
    plain_prompt: bool = False,
    mode: str = "quick",
    refresh: bool = False,
    reuse_root: Path | None = None,
    accept_review: str | None = None,
    register_capture: bool = False,
) -> Path:
    if not video_path.is_file():
        raise SystemExit(f"Video not found: {video_path}")
    if not prompt_path.is_file():
        raise SystemExit(f"Prompt file not found: {prompt_path}")
    try:
        media_capture.protect(video_path, output_path, (prompt_path,))
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if mode not in ("quick", "detailed"):
        raise SystemExit(f"Unknown capture mode: {mode}")
    video_prompt = prompt_path.read_text(encoding="utf-8")
    if not video_prompt.strip():
        raise SystemExit("Prompt is empty.")
    initial_media_hash = media_capture.sha(video_path)

    if plain_prompt or mode == "quick":
        system_instruction = video_prompt
        user_msg = "Analyze the attached video and return exactly the requested output."
    else:
        system_instruction = SYSTEM_INSTRUCTION_PREAMBLE + "\n" + video_prompt + SUBSTANCE_DELIVERABLE
        user_msg = "Analyze the attached video using the detailed instructions."
    capture_mode = "custom" if plain_prompt else mode
    capture_contract = media_capture.contract(
        "video", capture_mode, model, json.dumps([system_instruction, user_msg], ensure_ascii=False)
    )
    if register_capture:
        if accept_review is not None:
            raise ValueError("Register a pending capture before accepting its review.")
        try:
            existing = json.loads(media_capture.metadata_path(output_path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            existing = None
        if isinstance(existing, dict) and (existing.get("contract") != capture_contract
                                           or existing.get("media_sha256") != media_capture.sha(video_path)):
            raise ValueError("This capture's record names a different video or capture settings (mode, model or prompt); "
                             "register it only with those, or capture again.")
        media_capture.register(video_path, output_path, capture_contract, (prompt_path,))
        print(f"Pending review: {output_path}", flush=True)
        return output_path
    if accept_review is not None:
        media_capture.accept(video_path, output_path, capture_contract, accept_review, (prompt_path,))
        print(f"Reviewed for reuse: {output_path}", flush=True)
        return output_path
    if not refresh:
        match = media_capture.lookup(video_path, output_path, capture_contract, reuse_root, (prompt_path,))
        if match is not None:
            path, record = match
            canonical = media_capture.materialize(video_path, output_path, match, (prompt_path,))
            print(f"[{video_path.name}] REUSED — {canonical}; requested output: {output_path}; reviewed source: {record['source']} (record at {path})", flush=True)
            return canonical

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise SystemExit(
            "google-genai is not installed for "
            f"{sys.executable}. Run: {sys.executable} -m pip install google-genai"
        ) from exc

    api_key = resolve_gemini_api_key()
    client = genai.Client(api_key=api_key)

    # Handle emoji/non-ASCII filenames by copying to a safe path before upload.
    upload_source = video_path
    cleanup_safe_copy = False
    if needs_safe_filename(video_path):
        print(
            f"[{video_path.name}] Filename has non-ASCII chars; copying to safe path...",
            flush=True,
        )
        upload_source = copy_to_safe_path(video_path)
        cleanup_safe_copy = True

    upload = None
    try:
        print(f"[{video_path.name}] Uploading to Gemini...", flush=True)
        upload = client.files.upload(file=str(upload_source))
        upload = wait_for_active(client, upload)

        print(f"[{video_path.name}] Generating analysis (model={model})...", flush=True)
        response = client.models.generate_content(
            model=model,
            contents=[user_msg, upload],
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )
        text = getattr(response, "text", "") or ""
        if not text.strip():
            raise SystemExit("Gemini returned no capture text; previous output was preserved.")
        for candidate in getattr(response, "candidates", None) or []:
            reason = getattr(candidate, "finish_reason", None)
            if reason and str(getattr(reason, "name", reason)).split(".")[-1] != "STOP":
                raise SystemExit(
                    "Gemini did not finish normally; previous output was preserved."
                )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if media_capture.sha(video_path) != initial_media_hash:
            raise SystemExit("Source video changed during capture; previous output was preserved. Run again with the settled source.")
        content = (
            f"# Analysis: {video_path.name}\n\n"
            f"Capture mode: {capture_mode}; model: {model}. "
            f"Model output; not independently verified.\n\n{text}\n"
        )
        temporary_output = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="", dir=output_path.parent,
                prefix=".capture-", suffix=".tmp", delete=False,
            ) as handle:
                temporary_output = Path(handle.name)
                handle.write(content)
            # Invalidate an earlier approval before replacement, even if the text is identical.
            media_capture.register(video_path, output_path, capture_contract, (prompt_path,), content.encode("utf-8"))
            os.replace(temporary_output, output_path)
        finally:
            if temporary_output is not None:
                temporary_output.unlink(missing_ok=True)
        print(
            f"[{video_path.name}] DONE — {len(text):,} chars written to {output_path}",
            flush=True,
        )
        return output_path
    finally:
        if upload is not None:
            try:
                client.files.delete(name=upload.name)
            except Exception:
                pass
        if cleanup_safe_copy:
            try:
                upload_source.unlink()
            except Exception:
                pass


def default_output_path(video_path: Path, mode: str = "quick") -> Path:
    """Keep input extension and mode so distinct captures cannot collide."""
    return video_path.parent / "Analyses" / f"{video_path.name}.{mode}.md"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="Path to the video file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Output md path (default: <video-dir>/Analyses/<filename>.<mode>.md)",
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        help="Override the selected mode's prompt file",
    )
    parser.add_argument("--mode", choices=("quick", "detailed"), default="quick")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini model id (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--plain-prompt",
        action="store_true",
        help="Use the supplied prompt directly as the system instruction without ad-specific defaults",
    )
    parser.add_argument("--refresh", action="store_true", help="Recapture despite a reviewed match when source inspection shows a limitation")
    parser.add_argument("--reuse-root", type=Path, help="Also search this folder, which must contain the video, for reviewed captures of identical bytes")
    review_actions = parser.add_mutually_exclusive_group()
    review_actions.add_argument("--register-capture", action="store_true", help="Bind an existing or corrected full capture to its known source and capture settings as pending; no API call")
    review_actions.add_argument("--accept-review", metavar="NOTE", help="After source/coverage checks, accept the existing pending capture for reuse; no API call")
    args = parser.parse_args()

    video = args.video.expanduser().resolve()
    output = (
        args.output or default_output_path(video, "custom" if args.plain_prompt else args.mode)
    ).expanduser().resolve()
    prompt = (
        args.prompt or (QUICK_PROMPT_PATH if args.mode == "quick" else DEFAULT_PROMPT_PATH)
    ).expanduser().resolve()

    try:
        analyze(video, output, prompt, args.model, args.plain_prompt, args.mode,
                refresh=args.refresh, reuse_root=args.reuse_root, accept_review=args.accept_review,
                register_capture=args.register_capture)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot capture video: {error}\n")


if __name__ == "__main__":
    main()
