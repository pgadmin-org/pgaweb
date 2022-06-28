import datetime as dt

from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from blogs.models import Blog


class LatestEntriesFeed(Feed):
    title = "pgAdmin Blogs"
    link = reverse_lazy('blogs')
    description = "Blogs from the pgAdmin website."

    def items(self):
        return Blog.objects.filter(disable=False)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary + ' [<a href="{}">Read Blog</a>]'.\
            format(self.item_link(item))

    def item_link(self, item):
        return item.url

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return dt.datetime(item.date.year,
                           item.date.month,
                           item.date.day,
                           tzinfo=dt.timezone.utc)