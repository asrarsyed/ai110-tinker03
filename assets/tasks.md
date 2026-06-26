# Tasks — The Mood Machine

## Phase 1 — Build the dataset (`dataset.py`)
- [ ] Read existing `SAMPLE_POSTS` / `TRUE_LABELS` and confirm how they pair by index.
- [ ] Add 5–10 new posts to `SAMPLE_POSTS`.
  - [ ] Include at least one slang post ("lowkey", "no cap", "fire").
  - [ ] Include at least one emoji post (`🙂`, `💀`, `🥲`).
  - [ ] Include at least one sarcasm post ("love getting stuck in traffic").
  - [ ] Include at least one genuinely mixed post ("exhausted but proud").
  - [ ] Include at least one short/ambiguous post.
- [ ] Add one matching label to `TRUE_LABELS` for **every** new post.
- [ ] Verify `len(SAMPLE_POSTS) == len(TRUE_LABELS)`.
- [ ] Note any posts you'd disagree with a friend on (these are your edge cases).

## Phase 2 — Rule-based brain (`mood_analyzer.py`)
- [ ] **`preprocess`**: lowercase + strip, then strip punctuation from tokens.
- [ ] Decide and implement how to handle emojis (keep as tokens vs drop).
- [ ] Temporarily print tokens to confirm tokenization is correct.
- [ ] **`score_text`**: call `preprocess`, loop tokens, +1 for positive words, -1 for negative words, return total.
- [ ] Choose and implement **one** enhancement:
  - [ ] negation (look at `("not", "happy")` pairs), OR
  - [ ] word weighting (e.g. "hate" = -2), OR
  - [ ] emoji/slang as strong signals.
- [ ] **`predict_label`**: call `score_text`, map score → `positive` / `negative` / `neutral`.
- [ ] Add a `mixed` rule (e.g. both positive and negative hits present, or near-zero with signal).
- [ ] Test a clearly positive, clearly negative, and neutral sentence by hand.
- [ ] Remove temporary debug prints.
- [ ] (Optional) Confirm `explain()` still matches your scoring logic; uncomment `explain` lines in `main.py` if useful.

## Phase 3 — Stress test & break (`main.py` / `dataset.py` / `mood_analyzer.py`)
- [ ] Run `python main.py` and the interactive loop with 4+ breaker sentences.
- [ ] For each breaker, note which token dominated, which were ignored.
- [ ] Identify one clear failure pattern and write down why it happens.
- [ ] Make one small, targeted fix (vocab in `dataset.py` or logic in `mood_analyzer.py`).
- [ ] Re-run the same breaker; record whether it improved.
- [ ] Check the fix didn't regress earlier passing examples.

## Phase 4 — Evaluate (`main.py` + `ml_experiments.py`)
- [ ] Confirm every post has a label (re-check lengths).
- [ ] Run `python main.py`; record rule-based accuracy and the mismatches.
- [ ] Pick one wrong prediction and walk through the scoring step by step.
- [ ] Decide: fix it now, or document as a limitation (write down which).
- [ ] Run `python ml_experiments.py`; record ML accuracy and per-post predictions.
- [ ] Compare: do rule-based and ML fail on the same posts or different ones?
- [ ] Add a few more labeled posts; re-run both; note which model shifted more.

## Phase 5 — Model card (`model_card.md`)
- [ ] §1 Overview: state you used rule-based / ML / both, and the goal.
- [ ] §2 Data: post count, how you added/labeled them, hard-to-label cases.
- [ ] §3 Rule-based: exact scoring rules, your enhancement, thresholds, strengths/weaknesses.
- [ ] §4 ML: bag-of-words + logistic regression, training data, behavior on dataset changes.
- [ ] §5 Evaluation: accuracy numbers, 2–3 correct examples, 2–3 wrong examples.
- [ ] §6 Limitations: use real misclassified sentences from Phases 3–4, not generalities.
- [ ] §7 Ethics: bias/scope — whose language is this optimized for? who gets misread?
- [ ] §8 Improvements + a short rule-based vs ML comparison (fixes? new failures? data sensitivity?).
- [ ] Final read-through: a stranger could understand how it works, what shaped it, and where it breaks.
