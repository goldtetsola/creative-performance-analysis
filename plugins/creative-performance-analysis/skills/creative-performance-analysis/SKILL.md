---
name: creative-performance-analysis
license: MIT
description: Creative performance analysis. Find which ads earn spend, what in the creative explains it, and what to make next. Use when someone asks what creative is working, wants an account's high, low and zero-spend ads compared, or wants a named creative test reviewed.
---

# Creative performance analysis

Write a **creative analysis**: what creative sells for this brand right now, why buyers respond to it, and **blueprints** for what to make or change next. The reader is a creative strategist, or a media buyer working with creative. They want answers about creative; numbers are there when they ask. They take the blueprints into their own process. The analysis gives creative moves only: no budgets, bids, pausing, scaling, audiences or ad sets, and no ad copy, scripts or shot lists.

The analysis answers four questions:

1. Which ads earn the most spend, and what in their creative explains it against comparable ads?
2. Which get little or none, and is that the creative or a missing **fair fight**?
3. What separates the two ends, and which **exception** limits or sharpens that?
4. Do the results back up the leaders? When outcome data is supplied, use it to tell ads that sell from ads that only spend. Cost against a target, payback and first-order economics come up only when the user asks. Call an ad a "winner" only against a goal the user states; otherwise it is a "leader".

## Required reading

Every analysis runs every step, so every file in this table is required on every run. Read each in full before the step that uses it. A search hit, a skimmed section or a partial read is not a read. A required file never "doesn't apply": if a step would use it, it applies.

| Before step | Read in full |
|---|---|
| 2 | [evidence-rules.md](references/evidence-rules.md), [inspecting-ads.md](references/inspecting-ads.md) |
| 3 | [video-capture.md](references/video-capture.md), [ccs.md](references/ccs.md), [additional-lenses.md](references/additional-lenses.md), [growthcraft.md](references/growthcraft.md), [mindstates.md](references/mindstates.md) from "The four-part model" up to "Heuristics at a decision point", [hook-quality.md](references/hook-quality.md), [similarity.md](references/similarity.md), [reading-the-appeal.md](references/reading-the-appeal.md), [gain-and-loss-framing.md](references/gain-and-loss-framing.md) |
| 5 | [voice.md](references/voice.md), which sets how the analysis sounds; the user may have edited it |

Read these only when their condition holds:

- The category is crowded, the usual claims are worn, or buyers distrust them: [mature-market-response-chooser.md](references/mature-market-response-chooser.md).
- A decision shortcut, such as scarcity or social proof, informs a reading: "Heuristics at a decision point" in [mindstates.md](references/mindstates.md) and the catalogue entries it names.
- You name a mindstate profile: that whole profile in [mindstates.md](references/mindstates.md).

## 1. Set up the comparison

Fix the account or named test, its ads, dates, exclusions and the user's objective from the request and what they supplied. A named test is judged on its actual ads and run dates. A plan that hasn't launched stays a plan.

Use whatever the user provides: exports, screenshots, pasted tables, a connection their setup already has, ad files, links, reviews or notes. Then apply the **evidence gate**: every claim in the analysis stands on its own kind of evidence, and without it the analysis says what is missing and what it would answer instead of making the claim.

| Claim | Evidence it needs |
|---|---|
| What an ad shows or says, and any contrast, lesson, similarity verdict or blueprint built on it | That ad's inspected image, or its full video capture read whole and checked against the video where the claim depends on it |
| That two rows are the same ad, or which copy option ran | The same ad ID or a verified asset; delivery evidence for the copy. A shared name or a configured option is not enough |
| A creative lesson from two ads' results, including what a quiet run means | A fair fight between them |
| Anything about customers, orders or their value | Outcome data, read at the definition it has: credited orders are not people, and attributed is not caused |
| Why buyers care, stated as fact | Customer evidence in buyers' own words, which shows their stated reason, not what caused a result; otherwise it is a reading of the ad |
| Why the platform gave or withheld delivery, or how it groups ads | A verified constraint (rejected, paused, no budget, launched late) can be stated; anything else stays a hypothesis |

Intentions are not evidence of what ran. Ad names, labels, briefs, test plans and campaign notes say what someone meant the ad to be, not what it shows or did. They can locate a row; they cannot describe or group ads.

Ask for an input only when it would change the answer.

**Done when:** the comparison's ads, dates and objective are fixed, and every missing input is matched to the claims the gate blocks.

## 2. Map spend and results

Run `python3 scripts/csv_inventory.py <file>` on each CSV export before reading its values. Use `scripts/creative_metrics.py` for per-ad sums and ratios in its supported shape; other shapes get transparent calculations at their actual grain. Derive nested windows, such as the last 30, 14, 7 and 3 days, from one daily pull; they are not independent tests.

Build the spend map before choosing ads: spend, share of the population, impressions and outcomes where their bases are comparable. Keep currencies and incompatible populations apart.

A contrast between two ads teaches something about the creative only after a **fair fight**: comparable launch, eligibility, ad set and budget context in the period. Equal spend isn't required. A missing export row is not zero spend, and current status doesn't show past opportunity. An ad without a fair fight teaches nothing about the creative.

Select ads covering both ends of delivery, spend-versus-outcome disagreements, recent launches and the ads that break the pattern. Inspect every ad of a small named test. Expand the selection when a missing case could change a finding.

**Done when:** every selected ad has its figures on a stated basis and a fair-fight verdict, every zero is verified against the ad inventory, and what stays uninspected is recorded.

## 3. Inspect the ads

Inspect each selected ad as [inspecting-ads.md](references/inspecting-ads.md) describes. Every video you explain needs a full capture, read whole and checked against the video at the moments a claim rests on; quick captures only screen. Reuse a reviewed capture of the same bytes before making a new one. Capturing sends the user's video to Google's Gemini and costs API calls, so get the user's yes, naming how many videos, before the first upload ([video-capture.md](references/video-capture.md#run)); without it, explain only what images and existing captures allow.

Every explanation passes the evidence gate.

Judge each explained ad's opening with [hook-quality.md](references/hook-quality.md): who it stops, why they'd stay, and what sinks it. A blueprint's opening is held to the same test.

Find the **contrast**. When two ads share product, promise, page and a fair fight but differ in a moment, line or shot you can point to, that element is the difference that matters. How firmly it names the cause still depends on the result counts and on anything else that differs. Ads with different promises, offers or pages show which argument sells, with the other differences named beside the finding. A format label ("UGC beat studio") is where the search starts; the lesson is what the buyer sees, hears or learns. Check rivals that could change the finding: production, offer, page, opportunity, audience, timing and tracking.

Then hunt the **exception**: the ad that breaks your first version of the lesson. Let it sharpen the lesson.

Find why buyers care in the customer evidence: the want or doubt, in their words, and the moment the winning ad settles it.

Run the [similarity check](references/similarity.md) on the selected ads as one batch, for what they say and how they look.

**Done when:** every explained ad traces to its full capture or inspected image and its source rows; the contrast, the exception and the buyers' reason are each stated; every explained ad has an opening judgment from [hook-quality.md](references/hook-quality.md#using-it) (who it stops and why they might buy; which of feeling, gap and stakes it carries; promise or loop; anything that sinks it); and every inspected ad in the batch has a main motivation and a gain-or-loss reading, each resting on quoted words or a named visual moment, and a similarity verdict.

## 4. Choose the blueprints

Start from where the account is weakest: the products, buyers or spend the lesson doesn't reach yet, and the buyers, angles and formats no ad covers (the similarity check shows these). Then size each move: if it works, how much of what the brand sells could it change? A move that carries the lesson to products, buyers or spend that aren't working yet is **material**. Another version of an ad that already works, or a test that only explains why a winner won, is not, unless its answer would change what gets made across the account. Rank by the buyer decision each move could change and how much rides on it. Before keeping one, name what changes from the existing ad, what stays, why it beats the strongest alternative, and what its result could and could not show. When more than one thing changes, a win shows the new version works, not which change did it. A cheap test is high impact when its answer settles a creative choice that could change results; a move that only teaches ranks below one that could. A quiet run ends a version, not the idea behind it.

Each blueprint is one of three kinds, and says which: a **test** of the lesson, an **application** of it, or an **exploration** of something the ads haven't tried. A **repair** of something visibly wrong in an ad is a fourth kind and needs no result behind it. A test names its control, the existing ad it runs against. A blueprint built on a contrast passes the evidence gate: the contrast had a fair fight and its ads' captures were read whole. An ad without a fair fight teaches nothing about its results, so it can only get a repair.

Blueprints are creative only: new ads, edits to existing ads, and what to stop repeating. They never say which audience, ad set or customer group to run an ad to, how many versions to launch, or how to launch, schedule or set up a test; the reader runs that; "keep this for existing customers" is an account move.

**Done when:** the first blueprint is the most material move you found, with what it could reach named; each blueprint names its kind, its change, what stays, its control or strongest alternative, and what its result can and cannot settle, and its basis passes the evidence gate.

## 5. Check and write the analysis

Recompute every figure you use from its source on its declared basis ([check delivered figures](references/evidence-rules.md#check-delivered-figures-on-their-declared-basis)). Check every claim against the evidence gate and against its capture, image or source rows. Correct what fails and recheck what it touches.

Then write the analysis in the voice [voice.md](references/voice.md) sets, and deliver it the way that file says. The analysis carries meaning; the **Evidence** beneath it in the saved file carries measurement. Talk the reader through it in this flow, with a short heading for each part and the page shape [voice.md](references/voice.md) sets:

- **What sells and the contrast behind it:** the lesson first, pitched at the brand ("what sells right now is…") with this week's product as its example, then the ads that won and stalled during their fair fight and the exact moment or line that separates them, in words that carry the size of the split.
- **Why buyers care:** the want or doubt, in buyers' words when you have them, and how the winner settles it where the other ad doesn't.
- **The exception:** the ad that breaks the simple version, and what it teaches.
- **What to shoot or edit next:** the blueprints, best first, talked through as spoken advice. Each says what the ad is and which buyer it speaks to, what the opening must show and do and which existing moment or line it builds on, what changes and what stays, and how to read a win or a quiet run. An edit is plain actions with time ranges.
- **One thing to watch:** the similarity note: where the ads repeat each other in what they say or how they look, what that costs in reach, and the buyer, angle or format the next shoot should add.

A part the evidence gate blocks is one plain sentence saying what is missing and what it would answer. Mention ads, media or data left out only when they could change a call.

The Evidence holds every judgment the steps' "Done when" checks ask for, so each can be checked: each explained ad with its name, ID, what it shows, its opening judgment, its main motivation and gain-or-loss reading with the quoted words, its figures with period and basis, and its capture; the fair-fight verdicts and verified zeros; the similarity verdicts; the calculations and source files.

**Done when:** every figure and claim has passed its check; the analysis passes the read-aloud check in [voice.md](references/voice.md); every question above has an answer in it or a named evidence limit; and the Evidence holds every judgment the steps required.
