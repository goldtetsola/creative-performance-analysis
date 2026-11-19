# Creative performance analysis

A creative performance analysis for your agent. It finds which ads earn spend, explains why from the creative itself, and gives blueprints for what to make next. It gives creative moves only, never account or budget moves.

## Install

### Claude Code

```text
/plugin marketplace add goldtetsola/creative-performance-analysis
/plugin install creative-performance-analysis@rorschach
```

### Codex (not yet tested)

```shell
codex plugin marketplace add goldtetsola/creative-performance-analysis
codex plugin add creative-performance-analysis@rorschach
```

The Codex build ships the same skill and reading check, but it has not been tested in a live Codex session yet. Codex may ask you to trust the plugin's hook.

### Other agents

Copy `plugins/creative-performance-analysis/skills/creative-performance-analysis` into your agent's skills folder. Your agent needs to read files and run Python 3.11 or later. The reading check, which reminds the agent which references it still has to read, only comes with the Claude Code and Codex plugins.

## Set up video analysis

Video analysis uses Google's Gemini with your own key. It uploads each video you agree to analyse to Gemini and costs one API call per video; the agent asks before the first upload.

From the skill's folder (in a plugin install, ask your agent where it is):

```bash
python3 -m pip install -r requirements.txt
export GEMINI_API_KEY=your-key          # macOS / Linux
```

```powershell
$env:GEMINI_API_KEY = "your-key"        # Windows PowerShell
```

The footage similarity check needs `ffmpeg` and `ffprobe`. Everything else needs only Python.

## Use

Give the agent what you have, such as an Ads Manager export, screenshots, the ad videos and images, and customer reviews, and ask what creative is working and what to make next. You get the analysis in chat and a saved copy with the numbers and evidence beneath it. With fewer inputs you get a narrower analysis that says what's missing.

## Make it sound like you

`references/voice.md` inside the skill sets how the analysis sounds. Edit it to match your own style; the method and evidence rules don't change.

## License

MIT. See [LICENSE](LICENSE).
