# Plan — The Mood Machine

## Goal

Take a prototype sentiment analyzer (positive / negative / neutral / mixed) and:
1. Expand its dataset with realistic, messy language.
2. Implement the rule-based scoring brain.
3. Deliberately break it, then patch one failure.
4. Evaluate it against a labeled set and compare to a tiny ML model.
5. Document everything honestly in a model card.

The lesson is *why* simple AI tasks get brittle — sarcasm, slang, emojis, negation, ambiguity — not building a production classifier.

## Current state of the repo

- `dataset.py` — word lists + 6 labeled posts. Has TODO to add 5–10 more.
- `mood_analyzer.py` — `preprocess` is minimal; **`score_text` and `predict_label` are unimplemented (`pass`)**. `explain()` is already implemented and shows the simple +1/-1 logic to mirror.
- `main.py` — runs evaluation, batch demo, interactive loop. Already wired; needs the analyzer methods to work.
- `ml_experiments.py` — complete. CountVectorizer + LogisticRegression on the same dataset.
- `model_card.md` — template with 8 sections to fill.

> `main.py` runs without crashing even now, but since `predict_label` is `pass` it returns `None` for every post → all predictions print as `predicted=None` and accuracy is `0.00`. Implementing `score_text` + `predict_label` is the first real coding task.

## Phases

### Phase 1 — Dataset (Part 1)
Add 5–10 posts to `SAMPLE_POSTS` with matching `TRUE_LABELS`. Cover slang, emojis, sarcasm, mixed feelings, and ambiguous tone. Keep lengths equal. Goal: give both models richer (and harder) material.

### Phase 2 — Rule-based brain (Part 2)
Implement the three methods that data flows through:
- `preprocess` → consistent tokens (lowercase, strip punctuation, maybe split emojis).
- `score_text` → loop tokens, +1 positive / -1 negative, plus **one intentional enhancement**.
- `predict_label` → map score → label, with thresholds and a `mixed` rule.
Verify with obvious positive/negative/neutral sentences.

### Phase 3 — Stress test & patch (Part 3)
Write "breaker" sentences (sarcasm, slang, emoji, mixed). Find one clear failure pattern, make one small targeted fix in `dataset.py` or `mood_analyzer.py`, re-run, and note any regressions.

### Phase 4 — Evaluation (Part 4)
Run `python main.py` for rule-based accuracy and per-post predictions. Study mismatches. Run `python ml_experiments.py` and compare where each model fails. Add a few labeled posts and observe which model is more data-sensitive.

### Phase 5 — Model card (Part 5)
Fill `model_card.md` with concrete examples: how the dataset was built/labeled, the exact scoring rules, observed failures (with sentences), bias/scope notes, and a rule-based vs ML comparison.

## Key decisions to make

| Decision | Options | Notes |
|----------|---------|-------|
| Enhancement in `score_text` | negation handling / word weighting / emoji & slang signals | Pick **one** and do it well. Negation gives the most visible payoff. |
| Label thresholds | strict (`>0`/`<0`/`0`) vs banded (e.g. `>=2`) | Decide how a `mixed` label is produced (both pos & neg hits? near-zero score?). |
| Emoji strategy | ignore / treat as tokens / map to signals | Default `split()` drops attached emojis — decide if that matters. |
| Which failure to fix | sarcasm / slang / negation / emoji | Fix the one with the cleanest, smallest change. Document the rest. |
| Which errors to leave | — | Not every error is worth fixing; some are inherent rule-based limits. |

## Definition of done
- `python main.py` runs cleanly and prints predictions + accuracy.
- `python ml_experiments.py` runs cleanly.
- At least one documented break→fix story.
- `model_card.md` complete with specific, real examples.
