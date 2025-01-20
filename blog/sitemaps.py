from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from taggit.models import Tag
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
  
class TagSitemap(Sitemap):
  changefreq = 'daily'
  priority = 0.7

  def items(self):
    return Tag.objects.all()
  
  def location(self, obj):
    return reverse('blog:post_list_by_tag', kwargs={'tag_slug': obj.slug})
