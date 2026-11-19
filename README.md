# Creative strategy skills

Free creative strategy skills for your AI agent. Give it your ads and your results, and it tells you what creative sells, why buyers respond to it, and what to make next.

Built for creative strategists, and for media buyers who work with creative. Works in Claude Code and Codex, or any agent that can read files and run Python. MIT licensed.

Made by Gold Tetsola ([@gold_tesla](https://x.com/gold_tesla)). New skills land here over time. Watch the repo (Watch → All activity) or follow on X to hear when they do.

## The skills

| Skill | What it does |
|---|---|
| `creative-performance-analysis` | Compares the ads that earn spend with the ones that don't, finds the moment or line that makes the difference, and gives blueprints for what to shoot or edit next |

## What you get back

A creative analysis written the way a strategist would talk you through it. Numbers stay in a saved Evidence file underneath, so the read itself stays about creative. This excerpt is from a made-up account:

> **What sells right now is proof the buyer can check for themselves, not a promise they have to trust.**
>
> You can see it in Ad 21. It took almost all the prospecting spend and brought in most of the new customers this fortnight, while Ad 24, with the same bottle, page and ad set, barely spent.
>
> The difference is one moment. 21 pulls the bottle out of a hot car and shakes it so you hear the ice. 24 is a studio shot that writes "Cold for 24 hours" on screen and asks you to trust it.
>
> **1. The same check-it-yourself proof for the food jar.**
> The jar took about a third of the spend this fortnight on "keeps soup hot for 12 hours" written over a product shot, and almost nobody bought. Show someone opening it at their desk at lunch with the steam coming off the soup.

It gives creative moves only. It won't touch budgets, bids, audiences or launch settings, and it gives blueprints, not ad copy or scripts.

## Install

### Claude Code

```text
/plugin marketplace add goldtetsola/creative-strategy-skills
/plugin install creative-strategy@goldtetsola
```

Then ask it what creative is working. A run takes about 5 to 10 minutes.

### Codex

```shell
codex plugin marketplace add goldtetsola/creative-strategy-skills
codex plugin add creative-strategy@goldtetsola
```

The Codex build ships the same skills and reading check. When Codex asks you to trust the plugin's hook, allow it.

### Other agents

Copy the folders in `plugins/creative-strategy/skills/` into your agent's skills folder. Your agent needs to read files and run Python 3.11 or later. The reading check, which reminds the agent which references it still has to read, comes with the Claude Code and Codex plugins.

## What to give it

Whatever you have: an Ads Manager export or screenshots, the ad videos and images, and customer reviews. More inputs give a fuller read. With fewer, it says what's missing and what that would answer.

### Video analysis

Video analysis uses Google's Gemini with your own key. It uploads each video you agree to analyse and costs one API call per video; the agent asks before the first upload.

From the skill's folder (in a plugin install, ask your agent where it is):

```bash
python3 -m pip install -r requirements.txt
export GEMINI_API_KEY=your-key          # macOS / Linux
```

```powershell
$env:GEMINI_API_KEY = "your-key"        # Windows PowerShell
```

The footage similarity check needs `ffmpeg` and `ffprobe`. Everything else needs only Python.

## Make it sound like you

`references/voice.md` inside the skill sets how the analysis sounds. Edit it to match your own style; the method and evidence rules don't change.

## Work with me

The skills are free. If you'd rather have it done for you:

- **Creative analysis for your brand.** I go through your ads and results and tell you what's working, what isn't, and what to make next.
- **Ad account management.** I run your ad accounts and keep the creative and the spend pulling in the same direction.

DM me on X at [@gold_tesla](https://x.com/gold_tesla).

## Feedback

Found a bug, or a skill that gave bad advice? Open an issue with what you asked and what it did.

## License

MIT. See [LICENSE](LICENSE).
