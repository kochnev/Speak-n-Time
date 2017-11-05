from collections.languages.data import LANGUAGES
from main.models import Language

for lan in LANGUAGES:
    l = Language.objects.create(code=lan[0], name=lan[1])

