import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import brown

class English:
    def __init__(self):
        self.stemmer = SnowballStemmer("english", ignore_stopwords=True)
        self.SYNONYMS_THRESHOLD = 0.7
        self.freqs = nltk.FreqDist(w.lower() for w in brown.words())

    def get_synonyms(self, keyword_list):
        for keyword in keyword_list:
            for ss in wn.synsets(keyword):
                for lemma in ss.lemma_names():
                    if lemma.lower() != keyword.lower():
                        print(f"lemma {lemma}")
                        lemma1 = lemma.replace("_"," ")
                        print(lemma1)
                        print(self.freqs[lemma1])
                        key = wn.synsets(keyword)[0]
                        print(f"kry: {key}")
                        print(f"ss {ss}")
                        leema_sys = wn.synsets(lemma)[0]
                        lch = key.path_similarity(leema_sys)
                        print(lch)
                        print("*******")

    def stem_from_voice(self, sentence):
        stem_words = []
        for word in sentence.split():
            stem_words.append(self.stemmer.stem(word))
        new_sentence = " ".join(stem_words)
        return new_sentence

    def stem_keywrod_list(self, keyword_list):
        stem_words = []
        for word in keyword_list:
            stem_words.append(self.stemmer.stem(word))
        return stem_words



# class Hebrew:
#     # def __init__(self):
#
#
#     # def get_synonyms(self, keyword_list):
#     #
#     #
#     # def check_stamming_from_voice(self, sentence):
#
#     def stem_keywrod_list(self, keyword_list):





user_lan = English()
sen = "I love to walking to the mall and make my shopper"
keyword_list = ["AI", "Homeworks", "emails"]
user_lan.get_synonyms(keyword_list)
# user_lan.stem_from_voice(sen)
# user_lan.stem_keywrod_list(keyword_list)
# user_lan.get_all_hyponyms(keyword_list)
# user_lan.diff_method(keyword_list)