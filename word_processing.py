from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer

class English:
    '''
    Word processor for the English language
    '''
    def __init__(self):
        '''
        set the stemmer
        '''
        self.stemmer = SnowballStemmer("english", ignore_stopwords=True)

    def add_synonyms(self, keyword_list):
        '''
        Find one synonym for each word that has been goven by the user
        Args:
            keyword_list: keyword that have been given by the user
        Returns:
            the original words with the synonyms
        '''
        synonyms_keyword_list = []
        for keyword in keyword_list:
            for ss in wn.synsets(keyword):
                for lemma in ss.lemma_names():
                    lemma = lemma.replace("_", " ").lower()
                    if lemma != keyword.lower():
                        synonyms_keyword_list.append(lemma)
                        break
                else:
                    continue
                break
        return keyword_list + synonyms_keyword_list


    def stem_from_voice(self, sentence):
        '''
        Responsible for turning a sentence obtained from a transcript into a sentence which is consist only stemming words
        Args:
            sentence: a sentence obtained from a transcript

        Returns: Sentence which is consist only stemming words
        '''
        stem_words = []
        for word in sentence.split():
            stem_words.append(self.stemmer.stem(word))
        new_sentence = " ".join(stem_words)
        return new_sentence

    def stem_keywrod_list(self, keyword_list):
        '''
        Responsible for adding to the keyword_list the stem words
        Args:
            keyword_list: the keyword that have been given by the user
        Returns: list with the original keyword and the stem words
        '''
        stem_words = []
        for word in keyword_list:
            stem_word = self.stemmer.stem(word)
            if stem_word != word.lower():
                stem_words.append(stem_word)
        return keyword_list + stem_words

