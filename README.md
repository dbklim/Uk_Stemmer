# Ukrainian Stemmer

Это небольшая модификация стеммера для украинского языка [ukr_stemmer](https://github.com/Amice13/ukr_stemmer) от [Amice13](https://github.com/Amice13) на Python, добавляющая возможность простой установки стеммера через pip в качестве пакета python и немного упрощающая его использование.

[ukr_stemmer](https://github.com/Amice13/ukr_stemmer) от [Amice13](https://github.com/Amice13) является адаптированной реализацией [стеммера на Drupal от Algenon](https://drupal.org/project/ukstemmer) (4algenon@gmail.com).

[Стемминг](https://ru.wikipedia.org/wiki/Стемминг) - это процесс нахождения основы слова для заданного исходного слова. Основа слова не обязательно будет совпадать с морфологическим корнем слова. Стеммер - это конкретная реализация алгоритма стемминга. Стемминг используется в поисковых системах, в различных [NLP](https://ru.wikipedia.org/wiki/Обработка_естественного_языка)-задачах и является частью процесса нормализации текста.

## Установка

Установка с помощью pip:
```
pip install git+https://github.com/Desklop/Uk_Stemmer
```

Установка из исходных файлов:
```
git clone https://github.com/Desklop/Uk_Stemmer
cd Uk_Stemmer
pip install -e .
```

## Использование

Стеммер состоит из класса [UkStemmer](https://github.com/Desklop/Uk_Stemmer/blob/master/uk_stemmer/uk_stemmer.py#L32), который содержит метод [stem_word()](https://github.com/Desklop/Uk_Stemmer/blob/master/uk_stemmer/uk_stemmer.py#L69), выполняющий стемминг слова. Данный метод принимает слово в виде строки и возвращает найденную стемму (основу) данного слова так же в виде строки.

Простой пример для стемминга каждого слова в строке:
```python
import re
from uk_stemmer import UkStemmer

stemmer = UkStemmer()
test_string = 'Привіт, як твої справи? Зберігайте спокойствіе. Будь ласка, зберігайте спокій.'

prepare_test_string = test_string.lower()
words = re.split(r'(\W)', prepare_test_string)
words = [word for word in words if word != '']

for i in range(len(words)):
    words[i] = stemmer.stem_word(words[i])

stem_test_string = ''.join(words)
print('Source: %s\nStemmed: %s' % (test_string, stem_test_string))
```

---

Если у вас возникнут вопросы или вы хотите сотрудничать, можете написать мне на почту: vladsklim@gmail.com или в [LinkedIn](https://www.linkedin.com/in/vladklim/).