##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.db.backends.postgresql import base
import tsvector_field


class DatabaseWrapper(base.DatabaseWrapper):
    SchemaEditorClass = tsvector_field.DatabaseSchemaEditor
