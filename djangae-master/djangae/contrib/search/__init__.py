from django.utils.module_loading import autodiscover_modules

from . import model_document
from .index import Index  # noqa
from .document import Document  # noqa
from .model_document import (  # noqa
    ModelDocument,
    register,
)

from .fields import (  # noqa
    IntegrityError,
    TextField,
    NumberField,
    DateField,
    FuzzyTextField
)

default_app_config = 'djangae.contrib.search.apps.SearchConfig'


def autodiscover():
    # This will find all the search.py modules and add them to model_document._registry
    # The act of importing them will call any register(model, document) statements
    # in that file.
    autodiscover_modules('search', register_to=model_document)
