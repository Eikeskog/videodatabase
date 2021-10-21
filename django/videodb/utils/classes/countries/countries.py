import pandas as pd
import sys

countries_zip_path = (
    sys.path[0] + "\\countries.zip"
)  # videodb\\utils\\classes\\countries\\countries.zip'

INDEXED_LANGUAGES = [
    "no",
    "sv",
    "da",
    "de",
    "es",
    "fr",
    "en",
    "zh",
    "hi",
    "ar",
    "bn",
    "ru",
    "pt",
]


class NotSupportedError(Exception):
    def __init__(self, language_code=None, country_code=None):
        self.message = " code not supported: "
        if language_code:
            self.message = "Language" + self.message + language_code
        else:
            self.message = "Country" + self.message + country_code
        super().__init__(self.message)


class Countries:
    _countries = pd.read_csv(countries_zip_path).to_dict()
    _languages = INDEXED_LANGUAGES
    _indexes = {lang_code: i for i, lang_code in enumerate(_languages)}

    @classmethod
    def _get_lang_index(cls, lang_code):
        return cls._indexes[lang_code]

    @classmethod
    def get_translation(cls, country_code, lang_code):
        if country_code not in cls._countries:
            raise NotSupportedError(country_code=country_code)
        if lang_code not in cls._languages:
            raise NotSupportedError(language_code=lang_code)

        return cls._countries[country_code][cls._get_lang_index(lang_code)]


class Country:
    def __init__(self, country_code, language_code="en"):
        self._country_code = country_code.upper()
        self._language_code = language_code.lower()
        self._translated_name = Countries.get_translation(
            self._country_code, self._language_code
        )

    def __str__(self):
        return self._translated_name

    def language_code(self):
        return self._language_code

    def country_code(self):
        return self._country_code

    def translate_to(self, language_code):
        self._language_code = language_code.lower()
        self._translated_name = Countries.get_translation(
            self._country_code, self._language_code
        )
        return self._translated_name


# Examples:
# norway = Country('NO')

# print(norway)
# Norway

# print(norway.translate_to('es'))
# Noruega

# print(norway.translate_to('no'))
# Norge

# print(norway.translate_to('zh'))
# 挪威
