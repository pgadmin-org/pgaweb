##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from django.utils.functional import SimpleLazyObject

from docs.models import Page
from pgaweb import settings

def get_docs(request):
    pages = Page.objects.filter(version__active=True,
                                version__package__active=True,
                                file='index.html')

    return {'docs': pages}


def _get_gitrev():
    # Return the current git revision, that is used for
    # cache-busting URLs.
    try:
        with open('.git/refs/heads/master') as f:
            return f.readline()[:8]
    except IOError:
        # A "git gc" will remove the ref and replace it with a packed-refs.
        try:
            with open('.git/packed-refs') as f:
                for l in f.readlines():
                    if l.endswith("refs/heads/master\n"):
                        return l[:8]
                # Not found in packed-refs. Meh, just make one up.
                return 'ffffffff'
        except IOError:
            # If packed-refs also can't be read, just give up
            return 'eeeeeeee'


# Template context processor to add information about the root link and
# the current git revision. git revision is returned as a lazy object so
# we don't spend effort trying to load it if we don't need it (though
# all general pages will need it since it's used to render the css urls)
def PGAWebContextProcessor(request):
    gitrev = SimpleLazyObject(_get_gitrev)
    return {
        'gitrev': gitrev,
        'apps': settings.INSTALLED_APPS
    }
