from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
  changefreq = 'weekly'
  priority = 0.9
  # maximum value 1

  def items(self):
    # returns the queryset of objects to include in the sitemap
    return Post.published.all()

  def lastmod(self, obj):
    # receives each object returned by items() and returns the last time the object was modified
    return obj.updated