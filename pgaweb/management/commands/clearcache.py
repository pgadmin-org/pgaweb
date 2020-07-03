from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Clear the site-wide cache."""
    help = 'Clear the site-wide cache.'

    def handle(self, *args, **kwargs):
        try:
            assert settings.CACHES
            cache.clear()
            self.stdout.write('The cache has been cleared.\n')
        except AttributeError:
            raise CommandError('There is no cache configured.\n')