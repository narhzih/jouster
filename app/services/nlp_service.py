import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag


class NLPService:
    def __init__(self):
        try:
            nltk.data.find("tokenizers/punkt")
            nltk.data.find("corpora/stopwords")
            nltk.data.find("taggers/averaged_perceptron_tagger")
        except LookupError:
            nltk.download("punkt", quiet=True)
            nltk.download("stopwords", quiet=True)
            nltk.download("averaged_perceptron_tagger", quiet=True)

        self.stop_words = set(stopwords.words("english"))

    def extract_keywords(self, text: str) -> list[str]:
        if not text.strip():
            return ["text", "content", "analysis"]

        tokens = word_tokenize(text.lower())
        pos_tags = pos_tag(tokens)

        nouns = [
            word
            for word, pos in pos_tags
            if (
                pos.startswith("NN")
                and word.isalpha()
                and len(word) > 2
                and word not in self.stop_words
            )
        ]

        if not nouns:
            return ["content", "text", "information"]

        most_common = Counter(nouns).most_common(3)
        return [word for word, _ in most_common]


nlp_service = NLPService()
