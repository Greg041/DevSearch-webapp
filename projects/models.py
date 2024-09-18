# Django imports
from django.db import models
# Local imports
from users.models import Profile
# Third party imports
from cloudinary.models import CloudinaryField
import uuid


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = CloudinaryField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', '-created']

    def __str__(self):
        return self.title

    @property
    def get_votes_total(self):
        reviews = self.review_set.all()
        upvotes = reviews.filter(value='up').count()
        self.vote_total = reviews.count()
        self.vote_ratio = (upvotes / self.vote_total) * 100
        self.save()

    @property
    def reviewers_list(self):
        reviewers_id = self.review_set.all().values_list('owner__id', flat=True)
        return reviewers_id

    @property
    def get_image_url(self):
        try:
            image_url = self.featured_image.url
        except:
            image_url = ''
        return image_url
    


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        unique_together = [['owner', 'project'] ]

    def __str__(self):
        return self.value



