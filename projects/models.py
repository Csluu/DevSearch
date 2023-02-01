from django.db import models
import uuid
from users.models import Profile

# Create your models here.
class Project(models.Model):
    # many to one relationship 
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # many to many relationship - getting the Tag class below
    # don't have to use quotations ('') for Tag but since the class is below Projects we have to use quotations ('')
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True) 
    # will automatically create a time stamp when made- auto_now_add 
    created = models.DateTimeField(auto_now_add=True)
    # uuid will autogenerate a 64 character string, gives us a unique id  
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        # - orders it by descending by vote ratio first then how many votes it has if it has neither then it is by date created
        ordering = ['-vote_ratio', '-vote_total', '-created']
        
    @property
    def reviewers(self):
        # gives us the list of reviewers
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
        
        
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    # keeping it null=True because we have fake profiles at the moment
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, )
    # on_delete will delete all the reviews(child) for a project(parent) if project is deleted
    # foreign key establishes a one to many relationship 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        # makes it so that only a person can only make one review for a project
        unique_together =[['owner', 'project']]
    
    def __str__(self):
        return self.value
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name