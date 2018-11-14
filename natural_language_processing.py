from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

class Sentiment:
    def __init__(self):
        pass

    def runSimpleAnalysis(self, sentence):
        """
        Originally: demo_liu_hu_lexicon from: https://www.nltk.org/_modules/nltk/sentiment/util.html#demo_liu_hu_lexicon

        This function simply counts the number of positive, negative and neutral words
        in the sentence and classifies it depending on which polarity is more represented.
        Words that do not appear in the lexicon are considered as neutral.

        :param sentence: a sentence whose polarity has to be classified.
        """

        tokenizer = treebank.TreebankWordTokenizer()
        pos_words = 0
        neg_words = 0
        tokenized_sent = [word.lower() for word in tokenizer.tokenize(sentence)]

        for word in tokenized_sent:
            if word in opinion_lexicon.positive():
                pos_words += 1
            elif word in opinion_lexicon.negative():
                neg_words += 1

        if pos_words > neg_words:
            return('Positive')
        elif pos_words < neg_words:
            return('Negative')
        elif pos_words == neg_words:
            return('Neutral')
