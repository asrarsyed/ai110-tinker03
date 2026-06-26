# Codebase — The Mood Machine

The repo already exists. This is an architecture guide to how the pieces fit and where your work goes.

## Structure

```
ai110-tinker03/
├── dataset.py          # Single source of truth: word lists + labeled posts
├── mood_analyzer.py    # Rule-based classifier (the "brain" you implement)
├── main.py             # Entry point for the rule-based model
├── ml_experiments.py   # ML classifier (scikit-learn) on the same data
├── model_card.md       # Documentation deliverable
├── requirements.txt    # scikit-learn, matplotlib, ipykernel
├── plan.md             # Phased approach (this assignment)
├── tasks.md            # Granular TODOs
└── notes.md            # Concepts, gotchas, edge cases
```

## How it connects

```
                 dataset.py
        (POSITIVE_WORDS, NEGATIVE_WORDS,
         SAMPLE_POSTS, TRUE_LABELS)
            │                     │
            │ words + posts       │ posts + labels
            ▼                     ▼
     mood_analyzer.py        ml_experiments.py
     (MoodAnalyzer)          (CountVectorizer +
            │                 LogisticRegression)
            ▼                     │
        main.py  ◄────────────────┘
   (evaluate, demo, interactive)   both consume the same dataset,
                                   so editing dataset.py changes both
```

`dataset.py` is the hub. Both models import from it, which is the whole point: the same data drives two different approaches, and you can see how data choices ripple into each.

## File-by-file

### `dataset.py` — data layer
- `POSITIVE_WORDS` / `NEGATIVE_WORDS`: starter vocab the rule-based model matches against.
- `SAMPLE_POSTS`: example posts (index-aligned with labels).
- `TRUE_LABELS`: human label per post (`positive` / `negative` / `neutral` / `mixed`).
- **Invariant:** `len(SAMPLE_POSTS) == len(TRUE_LABELS)`.
- **You edit:** add 5–10 posts + labels here (Phase 1); maybe add vocab/slang/emojis (Phase 3).

### `mood_analyzer.py` — rule-based engine
`MoodAnalyzer` stores the word lists as lowercase sets. Three methods form the pipeline:
- `preprocess(text) -> List[str]` — text to tokens. *Minimal now; you improve it.*
- `score_text(text) -> int` — sum signals into a score. **Unimplemented (`pass`) — you write it + one enhancement.**
- `predict_label(text) -> str` — score to label. **Unimplemented (`pass`) — you write the mapping.**
- `explain(text) -> str` — already implemented; shows baseline +1/-1 reasoning and hits. Use it as a reference and for debugging output.

### `main.py` — rule-based runner (already wired)
- `evaluate_rule_based()` — prints predicted vs true per post, returns accuracy.
- `run_batch_demo()` — predictions only.
- `run_interactive_loop()` — type sentences live; `quit` to exit.
- Runs all three in sequence under `__main__`. Won't produce sensible output until `MoodAnalyzer` methods are implemented.

### `ml_experiments.py` — ML runner (complete)
- `train_ml_model()` — `CountVectorizer` (bag of words) + `LogisticRegression`. Raises on length mismatch / empty data.
- `evaluate_on_dataset()` — predicted vs true per post + accuracy (**note: training accuracy — same data it trained on**).
- `predict_single_text()` / `run_interactive_loop()` — single + interactive prediction.
- No changes required; you run it and compare. It reacts to your `dataset.py` edits automatically.

### `model_card.md` — documentation deliverable
8 sections (overview, data, rule-based, ML, evaluation, limitations, ethics, improvements). Fill with concrete examples from your runs. Final artifact a reader uses to understand the system.

## Where each phase touches the code

| Phase | Primary files |
|-------|---------------|
| 1 Dataset | `dataset.py` |
| 2 Rule-based brain | `mood_analyzer.py` (+ run `main.py`) |
| 3 Stress test | `dataset.py` and/or `mood_analyzer.py` |
| 4 Evaluate | run `main.py` + `ml_experiments.py` |
| 5 Model card | `model_card.md` |

## Setup

```bash
pip install -r requirements.txt
python main.py             # rule-based
python ml_experiments.py   # ML
```
