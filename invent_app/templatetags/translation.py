# custom_tags.py

from django import template
from django.utils.translation import gettext as _
from translate import Translator
from invent import settings

register = template.Library()

@register.simple_tag
def translate_string(string):
    language_code = getattr(settings, 'LANGUAGE_CODE', 'en-US')  # Get the language code from settings, defaulting to 'en'
    translator = Translator(to_lang=language_code)  # Initialize translator with the language code
    output = _(string)  # Get the string to be translated
    translation = translator.translate(output)  # Translate the string
    return _(translation)
