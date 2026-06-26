# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional
import re

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()

        # Expand common negation contractions so downstream scoring can
        # reliably detect patterns like "not happy".
        negation_expansions = {
            "don't": "do not",
            "doesn't": "does not",
            "didn't": "did not",
            "can't": "can not",
            "couldn't": "could not",
            "won't": "will not",
            "wouldn't": "would not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "haven't": "have not",
            "hasn't": "has not",
            "hadn't": "had not",
            "shouldn't": "should not",
            "mustn't": "must not",
            "mightn't": "might not",
            "needn't": "need not",
        }
        for contraction, expansion in negation_expansions.items():
            cleaned = re.sub(rf"\b{re.escape(contraction)}\b", expansion, cleaned)

        allowed_emojis = [":)", ":-(", "🥲", "😂"]
        emoji_placeholders = {
            emoji: f"EMOJI_TOKEN_{idx}" for idx, emoji in enumerate(allowed_emojis)
        }
        for emoji, placeholder in emoji_placeholders.items():
            cleaned = cleaned.replace(emoji, f" {placeholder} ")

        # Remove punctuation/symbols, including apostrophes.
        cleaned = re.sub(r"[^\w\s]", " ", cleaned)
        # Normalize whitespace across spaces/tabs/newlines.
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        raw_tokens = cleaned.split(" ") if cleaned else []
        tokens: List[str] = []

        placeholder_to_emoji = {v: k for k, v in emoji_placeholders.items()}
        for token in raw_tokens:
            if not token:
                continue

            if token in placeholder_to_emoji:
                tokens.append(placeholder_to_emoji[token])
                continue

            normalized = re.sub(r"(.)\1{2,}", r"\1\1", token)
            if normalized:
                tokens.append(normalized)

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)
        score = 0

        positive_weights = {
            "love": 2,
            "awesome": 2,
            "amazing": 2,
            "excited": 2,
        }
        negative_weights = {
            "hate": -2,
            "terrible": -2,
            "awful": -2,
            "angry": -2,
            "upset": -2,
            "stressed": -2,
        }
        emoji_and_slang_weights = {
            ":)": 2,
            "😂": 2,
            ":-(": -2,
            "🥲": -2,
            "lol": 1,
            "lmao": 1,
        }
        negation_tokens = {"not", "never", "no"}

        def token_score(token: str) -> int:
            if token in emoji_and_slang_weights:
                return emoji_and_slang_weights[token]
            if token in self.positive_words:
                return positive_weights.get(token, 1)
            if token in self.negative_words:
                return negative_weights.get(token, -1)
            return 0

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Flip the sentiment of a directly following sentiment token.
            if token in negation_tokens and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                next_score = token_score(next_token)
                if next_score != 0:
                    score -= next_score
                    i += 2
                    continue

            score += token_score(token)
            i += 1

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------
    
    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)
        tokens = self.preprocess(text)

        negation_tokens = {"not", "never", "no"}
        negated: set = set()
        i = 0
        while i < len(tokens):
            if tokens[i] in negation_tokens and i + 1 < len(tokens):
                negated.add(tokens[i + 1])
                i += 2
                continue
            i += 1

        token_set = set(tokens) - negated
        has_positive = bool(token_set & self.positive_words)
        has_negative = bool(token_set & self.negative_words)

        if has_positive and has_negative:
            return "mixed"
        if score >= 1:
            return "positive"
        if score <= -1:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)
        score = self.score_text(text)
        label = self.predict_label(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        negated_hits: List[str] = []

        negation_tokens = {"not", "never", "no"}
        emoji_and_slang_weights = {":)": 2, "😂": 2, ":-(": -2, "🥲": -2, "lol": 1, "lmao": 1}

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in negation_tokens and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if (
                    next_token in self.positive_words
                    or next_token in self.negative_words
                    or next_token in emoji_and_slang_weights
                ):
                    negated_hits.append(f"not {next_token}")
                    i += 2
                    continue
            if token in self.positive_words or (token in emoji_and_slang_weights and emoji_and_slang_weights[token] > 0):
                positive_hits.append(token)
            elif token in self.negative_words or (token in emoji_and_slang_weights and emoji_and_slang_weights[token] < 0):
                negative_hits.append(token)
            i += 1

        parts = [f"Score = {score}, label = {label!r}"]
        parts.append(f"positive: {positive_hits if positive_hits else []}")
        parts.append(f"negative: {negative_hits if negative_hits else []}")
        if negated_hits:
            parts.append(f"negated: {negated_hits}")
        return " | ".join(parts)
