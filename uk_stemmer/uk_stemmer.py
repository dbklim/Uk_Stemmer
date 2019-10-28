#!/usr/bin/python3
# -*- coding: utf-8 -*-
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#       OS : GNU/Linux Ubuntu 16.04 or 18.04
# LANGUAGE : Python 3.5.2 or later
#   AUTHOR : Klim V. O.
#     DATE : 28.10.2019
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

'''
Designed for stemming (taking the basis) of words of the Ukrainian language.
Is a slightly 'groomed' version of ukr_stemmer (https://github.com/Amice13/ukr_stemmer).

Contains the UkStemmer class. Read more in https://github.com/Desklop/Uk_Stemmer.

Based on:
1. Russian stemming algorithm provided by Dr Martin Porter:
http://snowball.tartarus.org/algorithms/russian/stemmer.html
2. Algorithm implementation in PHP provided by Dmitry Koterov:
http://forum.dklab.ru/php/advises/HeuristicWithoutTheDictionaryExtractionOfARootFromRussianWord.html
3. Algorithm implementation adopted for Drupal by Algenon (4algenon@gmail.com):
https://drupal.org/project/ukstemmer
'''

import re
import time


__version__ = 1.0


class UkStemmer():
    ''' Allows you to perform stemming of words of the Ukrainian language (that is, obtaining the basis of the word).
    Contains a single stem_word() method.

    Is a slightly 'groomed' version of the stemmer from Amice13: https://github.com/Amice13/ukr_stemmer '''
    def __init__(self):
        # http://uk.wikipedia.org/wiki/Голосний_звук
        self.vowel = r'аеиоуюяіїє'
        self.perfectiveground = r'(ив|ивши|ившись|ыв|ывши|ывшись((?<=[ая])(в|вши|вшись)))$'
        # http://uk.wikipedia.org/wiki/Рефлексивне_дієслово
        self.reflexive = r'(с[яьи])$'
        # http://uk.wikipedia.org/wiki/Прикметник + http://wapedia.mobi/uk/Прикметник
        self.adjective = r'(ими|ій|ий|а|е|ова|ове|ів|є|їй|єє|еє|я|ім|ем|им|ім|их|іх|ою|йми|іми|у|ю|ого|ому|ої)$'
        # http://uk.wikipedia.org/wiki/Дієприкметник
        self.participle = r'(ий|ого|ому|им|ім|а|ій|у|ою|ій|і|их|йми|их)$'
        # http://uk.wikipedia.org/wiki/Дієслово
        self.verb = r'(сь|ся|ив|ать|ять|у|ю|ав|али|учи|ячи|вши|ши|е|ме|ати|яти|є)$'
        # http://uk.wikipedia.org/wiki/Іменник
        self.noun = r'(а|ев|ов|е|ями|ами|еи|и|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я|і|ові|ї|ею|єю|ою|є|еві|ем|єм|ів|їв|ю)$'
        self.rvre = r'[аеиоуюяіїє]'
        self.derivational = r'[^аеиоуюяіїє][аеиоуюяіїє]+[^аеиоуюяіїє]+[аеиоуюяіїє].*(?<=о)сть?$'
        self.RV = ''


    def __ukstemmer_search_preprocess(self, word):
        word = word.lower()
        word = word.replace("'", "")
        word = word.replace("ё", "е")
        word = word.replace("ъ", "ї")
        return word


    def __s(self, st, reg, to):
        orig = st
        self.RV = re.sub(reg, to, st)
        return (orig != self.RV)


    def stem_word(self, word):
        ''' Find the basis (stem) of a word.
        1. word - source word (UTF-8 encoded string)
        2. returns the stemmed form of the word (UTF-8 encoded string) '''

        word = self.__ukstemmer_search_preprocess(word)
        if not re.search('[аеиоуюяіїє]', word):
            stemma = word
        else:
            p = re.search(self.rvre, word)
            start = word[0:p.span()[1]]
            self.RV = word[p.span()[1]:]

            # Step 1
            if not self.__s(self.RV, self.perfectiveground, ''):

                self.__s(self.RV, self.reflexive, '')
                if self.__s(self.RV, self.adjective, ''):
                    self.__s(self.RV, self.participle, '')
                else:
                    if not self.__s(self.RV, self.verb, ''):
                        self.__s(self.RV, self.noun, '')
            # Step 2
            self.__s(self.RV, 'и$', '')

            # Step 3
            if re.search(self.derivational, self.RV):
                self.__s(self.RV, 'ость$', '')

            # Step 4
            if self.__s(self.RV, 'ь$', ''):
                self.__s(self.RV, 'ейше?$', '')
                self.__s(self.RV, 'нн$', u'н')

            stemma = start + self.RV
        return stemma
    

    def stemWord(self, word):
        ''' Find the basis (stem) of a word.
        1. word - source word (UTF-8 encoded string)
        2. returns the stemmed form of the word (UTF-8 encoded string)
        
        This method is used to simulate the PyStemmer interface (https://github.com/snowballstem/pystemmer). '''

        return self.stem_word(word)




def main():
    stemmer = UkStemmer()
    test_string = 'Привіт,як твої  справи?  (це ж тест??) Зберігайте спокойствіе.Оплатіте ласка, зробіть погашення боргу/заборгованостей. ' + \
                  'Рефлексивного и тямущий'

    start_time = time.time()
    prepare_test_string = test_string.lower()
    words = re.split(r'(\W)', prepare_test_string)
    words = [word for word in words if word != '']

    for i in range(len(words)):
        words[i] = stemmer.stem_word(words[i])

    stem_test_string = ''.join(words)
    work_time = time.time() - start_time

    print('Source: %s\nStemmed: %s\nTime: %.6f' % (test_string, stem_test_string, work_time))


if __name__ == '__main__':
    main()
