import requests
import sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


LANGS = ['arabic', 'german', 'english', 'spanish', 'french',
         'hebrew', 'japanese', 'dutch', 'polish', 'portuguese',
         'romanian', 'russian', 'turkish', 'all']
UA = UserAgent()
HEADERS = {'User-Agent': UA.random}

class WrongLangError(Exception):
    def __init__(self, lang):
        print(f"Sorry, the program doesn't support {lang}")


class WrongWordError(Exception):
    def __init__(self, word):
        print(f"Sorry, unable to find {word}")


def adv_print(text, file):
    print(text)
    print(text, file=file)


def get_translation(lang_from, lang_to, word, session=requests.Session()):
    URL = f"https://context.reverso.net/translation/{lang_from}-{lang_to}/{word}"

    response = session.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    with open(f"{word}.txt", mode='a', encoding='utf-8') as f:
        translations = soup.select("#translations-content > .translation")
        if not translations:
            raise WrongWordError(word)
        adv_print(f"\n{lang_to.title()} Translations:", f)
        for w in translations:
            adv_print(w.text.strip(), f)

        adv_print(f"\n{lang_to.title()} Examples:", f)
        examples_html = soup.find_all('div', {'class': 'example'})
        for ex2 in examples_html:
            pair = ex2.find_all('span', {'class': 'text'})
            example1, example2 = pair[0].text.strip(), pair[1].text.strip()
            adv_print(example1, f)
            adv_print(example2 + '\n', f)


def get_translation_to_all(lang_from, word):
    with requests.Session() as session:
        LANGS.remove(lang_from)
        LANGS.remove('all')
        for n in LANGS:
            get_translation(lang_from, n, word, session)


if __name__ == '__main__':
    try:
        args = sys.argv
        lang_from = args[1]
        lang_to = args[2]
        word = args[3]
        if (lang_from not in LANGS):
            raise WrongLangError(lang_from)
        if (lang_to not in LANGS):
            raise WrongLangError(lang_to)
        if lang_to == 'all':
            get_translation_to_all(lang_from, word)
        else:
            get_translation(lang_from, lang_to, word)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
    except WrongLangError:
        pass
    except WrongWordError:
        pass

