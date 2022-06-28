from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from news.models import News


class LatestEntriesFeed(Feed):
    title = "pgAdmin News"
    link = reverse_lazy('news')
    description = "News articles from the pgAdmin website."

    def items(self):
        return News.objects.filter(disable=False)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content + ' [<a href="{}">Read News</a>]'.\
            format(self.item_link(item))

    def item_link(self, item):
        return reverse_lazy('news') + '#' + str(item.id)
