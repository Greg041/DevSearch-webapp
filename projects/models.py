from django.db import models
from users.models import Profile

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="images/default.jpg", upload_to='images/')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

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

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', '-created']


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner', 'project'] ]

    def __str__(self):
        return self.value



