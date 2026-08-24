"""Vendorised copy of django-tsvector-field (a5f1c5b, 2019).

Does not work on Django 6: fields.py imports django.utils.itercompat.is_iterable,
which Django 6 removed, so importing this package fails and takes the custom
database engine in pgaweb/db with it. requirements.txt pins Django below 6 for
that reason. Fixing it means either updating this copy against upstream, or
moving to django.contrib.postgres.search.SearchVectorField, which is not a drop
in: the point of this library is that it maintains the tsvector column with
triggers, which the built-in field leaves to the caller.
"""

from .fields import SearchVectorField, WeightedColumn
from .schema import DatabaseSchemaEditor
from .query import Headline
from .operations import IndexSearchVector

default_app_config = 'tsvector_field.apps.TextSearchVectorConfig'
