from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from .models import BlogPost

exclude_posts = ("about", "projects", "talks")


class ExtendedRssFeed(Rss201rev2Feed):
    """
    Rss feed with content
    """
    mime_type = 'application/xml'

    def root_attributes(self):
        attrs = super(ExtendedRssFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRssFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])


class BlogPostFeed(Feed):
    feed_type = ExtendedRssFeed
    title = "laike9m's blog"
    link = "/blog/rss"
    description = "Update on laike9m blog's articles."

    def items(self):
        return BlogPost.objects.exclude(title__in=exclude_posts)[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return item.description or '没有简介, 请去看原文吧'

    def item_pubdate(self, item):
        return item.pub_date

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    def item_content_encoded(self, item):
        import re
        html = item.display_html()
        html = re.sub(r"/media/", r"http://laike9m.com/media/", html)
        return html
