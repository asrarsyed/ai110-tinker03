# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**  
Both models were implemented and compared. The rule based model was the primary focus; the ML model was used as a reference point.

**Intended purpose:**  
Classify short social-media-style text snippets into one of four mood labels: positive, negative, neutral, or mixed.

**How it works (brief):**  
The rule based model tokenizes input text, expands negation contractions, preserves emojis as special tokens, then scores each token using weighted positive/negative word lists and emoji/slang weights. Negation tokens ("not", "never", "no") flip the score of the following word. A sentence is labeled mixed if it contains both positive and negative words (after excluding negated tokens), otherwise the net score determines the label. The ML model converts text into bag-of-words vectors using CountVectorizer and trains a logistic regression classifier on those vectors and the true labels.



## 2. Data

**Dataset description:**  
The dataset contains 16 labeled posts in `SAMPLE_POSTS`. Posts were written to represent realistic social media language including slang, emojis, sarcasm, and mixed emotions. No additional posts were added beyond the starter set.

**Labeling process:**  
Labels were assigned by human judgment. Several posts were genuinely ambiguous. "I absolutely love getting stuck in traffic for an hour 😂" could be argued as mixed (sarcasm + humor) but was labeled negative. "Awesome, my laptop died right before the deadline." similarly reads as sarcastic negative. "Got the internship but now I'm scared I'll mess it up 🥲" was labeled mixed because it contains genuine positive and negative emotions.

**Important characteristics of your dataset:**

- Contains slang ("lowkey", "highkey", "no cap")
- Includes emojis used both literally and ironically (😂, 🥲, 💀)
- Includes sarcasm that inverts word-level sentiment
- Several posts express genuinely mixed feelings
- Some posts are short and low-signal ("This is fine", "Meh, just another Tuesday.")

**Possible issues with the dataset:**

- Only 16 examples total, severely limiting ML generalization
- 4 labels across 16 examples means ~4 examples per class on average
- Sarcasm is present but undetectable by word-level methods
- Label disagreement is possible on several edge cases
- Dataset skews toward informal English; formal or non-native phrasing not represented

## 3. How the Rule Based Model Works

**Scoring rules:**

- Each token matched in `POSITIVE_WORDS` adds +1 to the score; matched in `NEGATIVE_WORDS` subtracts -1
- High-signal words have custom weights: "love", "awesome", "amazing", "excited" score +2; "hate", "terrible", "awful", "angry", "upset", "stressed" score -2
- Emojis and slang have explicit weights: ":)" and 😂 score +2, ":-(" and 🥲 score -2, "lol" and "lmao" score +1
- Negation tokens ("not", "never", "no") flip the sign of the immediately following sentiment token and consume both tokens
- Negation contractions ("don't", "isn't", etc.) are expanded before tokenization so negation detection works consistently
- Label thresholds: score >= 1 → positive, score <= -1 → negative, score == 0 → neutral; if both positive and negative words are present in non-negated tokens → mixed (checked before score thresholds)

**Strengths:**

- Fully explainable: every prediction traces to specific tokens and weights
- Generalizes to unseen text as long as vocabulary matches
- Negation handling correctly flips "not happy" to negative
- Mixed label detection based on co-presence of positive and negative words works well for genuinely ambivalent sentences

**Weaknesses:**

- Cannot detect sarcasm ("I absolutely love getting stuck in traffic")
- Unknown words score zero and are silently ignored
- Single dominant token can override sentence context ("awesome" at +2 overpowers "died" at -1)
- Emoji handling limited to four pre-defined emojis; all others ignored
- No understanding of sentence structure or intent

## 4. How the ML Model Works

**Features used:**  
Bag of words using `CountVectorizer`. Each unique word in the training corpus becomes a feature; each sentence is represented as a word frequency vector.

**Training data:**  
Trained on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py` (16 examples).

**Training behavior:**  
The model achieved 1.00 accuracy on the training set. This is expected with 16 examples and no train/test split — the model memorizes the data rather than learning generalizable patterns. No accuracy changes were observed across runs because the dataset was not modified during ML experimentation.

**Strengths and weaknesses:**  
Strength: learns associations automatically without hand-crafted rules. Correctly labeled the sarcasm case ("love getting stuck in traffic") because it memorized the exact sentence. Weakness: 1.00 training accuracy is pure overfitting, not generalization. On unseen text, it would likely perform poorly. Bag of words loses word order, so negation ("not happy" vs "happy") is not represented. Requires retraining to handle new vocabulary.

## 5. Evaluation

**How you evaluated the model:**  
Both models were evaluated on the full `SAMPLE_POSTS` set using exact label match accuracy. The rule based model was iteratively improved by analyzing failure cases. The ML model was evaluated once on its training data.

**Examples of correct predictions:**

- "I am not happy about this" → negative. Negation expansion ("not happy") correctly flipped the positive score to negative.
- "Feeling tired but kind of hopeful" → mixed. Both "tired" (negative) and "hopeful" (positive) present, triggering mixed label.
- "Highkey annoyed my bus left early again 💀" → negative. Adding "annoyed" to NEGATIVE_WORDS fixed this case from an earlier neutral prediction.

**Examples of incorrect predictions:**

- "I absolutely love getting stuck in traffic for an hour 😂" → predicted positive, true negative. "love" (+2) and 😂 (+2) dominate; sarcasm undetectable at the word level.
- "Got the internship but now I'm scared I'll mess it up 🥲" → predicted negative, true mixed. "scared" (-1) and 🥲 (-2) sum to -3 with no positive word present; the positive sentiment (getting the internship) is carried by the word "internship" which is not in any word list.
- "Awesome, my laptop died right before the deadline." → predicted mixed, true negative. "awesome" is in POSITIVE_WORDS and "died" is in NEGATIVE_WORDS, triggering mixed; the model cannot detect that "awesome" is ironic here.

**Rule based final accuracy:** 0.81 (13/16 correct)  
**ML model training accuracy:** 1.00 (16/16, memorized)

## 6. Limitations

- Dataset is too small (16 examples) to draw reliable conclusions about either model's real-world performance
- Rule based model cannot detect sarcasm or irony under any word-level scoring scheme
- ML model has no real test set; 1.00 accuracy reflects memorization not learning
- Both models fail on vocabulary not seen during development
- Emoji coverage is limited to four hand-coded emojis; the vast majority of emojis have no effect
- Neither model handles multi-sentence input well; a long post with a topic shift would be scored as a single unit
- Models were tuned on the same dataset used for evaluation, introducing implicit overfitting even in the rule based model

## 7. Ethical Considerations

- Misclassifying distress as neutral or positive is a real risk. A message like "I'm fine, everything is fine" scoring neutral could mask depression or crisis signals in a mental health context.
- Slang and emoji conventions vary significantly across communities and age groups. A model trained on one dialect's informal language will systematically misclassify others.
- Sarcasm patterns differ across cultures. The current sarcasm failures would be worse on text from communities with different irony conventions.
- Mood detection on personal messages raises privacy concerns. Inferring emotional state from text without consent is a meaningful privacy intrusion even if the text is public.
- Automated mood classification at scale (content moderation, employee monitoring) could cause harm if acted upon without human review, especially given the accuracy limitations shown here.

## 8. Ideas for Improvement

- Add a real train/test split (e.g. 80/20) so ML accuracy reflects generalization not memorization
- Expand the dataset to at least 50-100 examples per label for meaningful ML training
- Use TF-IDF instead of CountVectorizer to downweight common words ("I", "the", "a") that carry no sentiment
- Add more emoji mappings, or use a Unicode emoji sentiment library
- Extend slang vocabulary ("lowkey", "highkey", "no cap", "fr", "deadass", "💀" as negative intensifier)
- For the rule based model: add an intensifier list ("absolutely", "really", "so") that multiplies the following word's score
- For sarcasm: look for patterns like positive word + negative context word nearby as a weak sarcasm signal
- Use a small pre-trained transformer (e.g. DistilBERT fine-tuned on sentiment) which already handles sarcasm and negation through context
