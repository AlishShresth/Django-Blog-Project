from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
# from django.db.models.function import Now

class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(models.Model):
    class Status(models.TextChoices):
      DRAFT = 'DF', 'Draft'
      PUBLISHED = 'PB', 'Published'
      # available choices are DRAFT and PUBLISHED, their respective values are DF and PB, and their labels or readable names are Draft and Published
      # use Post.Status.choices to obtain the available choices
      # use Post.Status.names to obtain the names of the choices
      # use Post.Status.labels to obtain the human-readable names
      # use Post.Status.values to obtain the actual values of the choices
      # you can import the Post model and use Post.Status.DRAFT as a reference for the DRAFT status anywhere in your code
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    # related_name is used to specify the name of the reverse relationship, from User to Post. 
    # user.blog_posts
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # publish = models.DateTimeField(db_default=Now())
    # to use database-generated default values, we use the db_default attribute instead of default
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # deleted = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager() # default manager
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        # default_manager_name = 'published'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
                ]
        )