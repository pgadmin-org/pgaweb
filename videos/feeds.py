import datetime as dt

from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from videos.models import Video


class LatestEntriesFeed(Feed):
    title = "pgAdmin Videos"
    link = reverse_lazy('videos')
    description = "Videos from the pgAdmin website."

    def items(self):
        return Video.objects.filter(disable=False)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description + ' [<a href="{}">Watch Video</a>]'.\
            format(self.item_link(item))

    def item_link(self, item):
        return 'https://www.youtube.com/watch?v=' + item.youtube_id

    def item_author_name(self, item):
        return item.publisher

    def item_pubdate(self, item):
        return dt.datetime(item.date.year,
                           item.date.month,
                           item.date.day,
                           tzinfo=dt.timezone.utc)
