# Notes — The Mood Machine

## Key concepts

- **Two paradigms, same data.** The rule-based model (`mood_analyzer.py`) follows logic *you* write. The ML model (`ml_experiments.py`) learns weights from labeled examples. Both read `SAMPLE_POSTS` / `TRUE_LABELS` from `dataset.py` — so the dataset is the shared lever that shapes both.
- **The score is just a number.** It summarizes what the model noticed (positives add, negatives subtract). No understanding of emotion is involved. `explain()` already demonstrates the baseline +1/-1 counting.
- **Data flow (rule-based):** `text → preprocess (tokens) → score_text (int) → predict_label (string)`. Each method depends on the previous one.
- **Bag of words (ML):** `CountVectorizer` turns each post into word-count vectors; `LogisticRegression` learns which words push toward which label. Word order and context are lost.

## Gotchas

- **`main.py` runs even before you implement anything — but uselessly.** `score_text` and `predict_label` are both `pass`, so `predict_label` returns `None` (it doesn't raise). Every post prints `predicted=None` and accuracy is `0.00`. No exception, no "helpful error" — just silently wrong until you implement both. This is the real first coding step, not just dataset edits.
- **Length mismatch crashes things.** `len(SAMPLE_POSTS)` must equal `len(TRUE_LABELS)`. `ml_experiments.py` raises `ValueError` explicitly; `main.py`'s `zip` silently truncates and gives wrong accuracy. Always re-check after edits.
- **`str.split()` doesn't strip punctuation.** `"day."` ≠ `"day"`, so the word won't match the vocab. Same for capitalization (handled) and attached emojis (`"fine🙂"` is one token).
- **Word lists are sets of lowercase words.** Multi-word slang ("no cap") and emojis won't match unless you add them and tokenize so they survive.
- **ML "accuracy" here is training accuracy.** `ml_experiments.py` evaluates on the same posts it trained on, so high accuracy ≈ memorization, not generalization. Don't over-trust the number.
- **Tiny dataset = unstable ML.** With ~10–16 examples and 4 classes, logistic regression overfits and a single label change can flip predictions. That sensitivity is part of the lesson.
- **`mixed` is the trap.** The starter mapping only emits positive/negative/neutral. If `TRUE_LABELS` contains `mixed`, the rule-based model can *never* score it correctly unless you add a `mixed` rule.

## Edge cases to test (breakers)

- **Sarcasm:** "I love getting stuck in traffic" → keyword "love" makes it look positive.
- **Negation:** "I am not happy about this" — without negation handling, "happy" scores +1 (wrong). This is already in the dataset labeled `negative`.
- **Slang polarity flips:** "sick", "wicked", "fire" can be positive or negative; not in the vocab at all.
- **Emojis:** "I'm fine 🙂" — emoji carries the tone but is dropped or unmatched.
- **Mixed emotion:** "exhausted but proud of myself" — one positive + one negative token nets to ~0 → wrongly "neutral".
- **Intensity:** "soooo happy" vs "happy" — repeated chars and "so" aren't weighted.
- **Empty / ambiguous:** "This is fine" — no vocab hits → score 0 → neutral (sometimes right, often not).

## Worth researching before starting

- Simple negation handling: scan token pairs, flip or zero the next sentiment word after "not"/"never"/"no".
- Punctuation stripping: `str.strip(string.punctuation)` per token, or a small regex tokenizer.
- Word weighting: a `dict` of word→weight instead of flat +1/-1.
- `CountVectorizer` defaults: it lowercases and strips punctuation, and drops 1-char tokens / emojis — so the ML model already won't "see" emojis either.
- Why accuracy alone misleads: class imbalance and train-on-test inflation.

## Working tips

- Print intermediate values (tokens, score, hits) while building; remove before finishing.
- Make one change at a time and re-run — easier to attribute behavior changes.
- Keep AI-assistant chats short and task-specific; treat suggested fixes as hypotheses to verify against the code, not answers.
- Run order: `python main.py` (rule-based) then `python ml_experiments.py` (ML). Both have interactive loops — type `quit` or empty line to exit.
- Install deps first: `pip install -r requirements.txt` (needs scikit-learn for the ML part).
