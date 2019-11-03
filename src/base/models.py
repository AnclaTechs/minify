from django.db import models
from django.db.models.signals import post_save
from minify.settings import AUTH_USER_MODEL
from tinymce import HTMLField
from django.urls import reverse
import datetime
from django.contrib.postgres.fields import JSONField
import json
from acctmang.models import Profile



#NOTES
NOTETYPE = (
    ("GEN", "GENERAL NOTE/PROBLEM/SOLUTION"),
    ("HTSS", "HTML/CSS"),
    ("PYTH", "PYTHON"),
    ("JS", "JAVASCRIPT"),
    ("C", "C/C++"),
    ("PHP", "PHP"),
    ("GO", "GOLANG"),
    ("RUBY", "RUBY"),
    ("JAVA", "JAVA")
)
class Note(models.Model):
    """
    Minify Notes- Users personal notes
    """
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="note")
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    notetype = models.CharField(choices=NOTETYPE, max_length=10, default="GEN")
    note = models.TextField()
    links = models.CharField(max_length=2000)
    public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(self.owner, self.created)


class QuestionTags(models.Model):
    """
    Tags for Questions
    """

    class Meta:
        verbose_name = "Question tag"
        verbose_name_plural = "Question tags"

    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name


class Questions(models.Model):
    """
    Public Questions
    """

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField()
    body = HTMLField('Content')
    views = models.IntegerField(default=0)
    created = models.DateTimeField(
        auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    #tags = models.ManyToManyField(QuestionTags)

    def __str__(self):
        return "{} : {}".format(self.owner, self.title)

    def get_absolute_url(self):
        return reverse('question-detail', args=[self.id, self.title])


class QueComment(models.Model):
    """
    Comment for Questions
    """
    class Meta:
        verbose_name = "Question-comment"
        verbose_name_plural = "Question-comments"

    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name="quecomments")
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=300, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.author, self.question)


class QueAnswer(models.Model):
    """
    Answers for Questions
    """

    class Meta:
        verbose_name = "Question-answer"
        verbose_name_plural = "Question-answer"

    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name="queanswers")
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = HTMLField('Content')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.author, self.created)

class Vote(models.Model):
    answer = models.OneToOneField(
        QueAnswer, on_delete=models.CASCADE, related_name="queanswervotes")
    users_vote = JSONField(null=True, default=dict)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    def __str__(self):
        return "{} : {}".format(self.answer, (self.upvote - self.downvote))

def create_vote(sender, **kwargs):
    if kwargs['created']:
        spin_vote = Vote.objects.create(answer=kwargs['instance'])


post_save.connect(create_vote, sender=QueAnswer)


class QueAnswerComment(models.Model):
    """
    Comments for QueAnswers
    """

    class Meta:
        verbose_name = "Question-answer Comment"
        verbose_name_plural = "Question-answer Comments"

    answer = models.ForeignKey(
        QueAnswer, on_delete=models.CASCADE, related_name="queanswercomments")
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=300, blank=False)
    created = models.DateTimeField(auto_now_add=True)


class Posts(models.Model):
    """
    Public Posts (to followers and recommended audience)
    """
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(max_length=300, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.owner, self.id)


class Like(models.Model):
    """
    Like(s) for public posts
    """
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="likes")
    created = models.DateTimeField(auto_now_add=True)


class PostsCommentary(models.Model):
    """
    Post as commentary to other Post
    """
    class Meta:
        verbose_name = "Post-Comment"
        verbose_name_plural = "Post-Comments"
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="postcommentary")
    body = models.TextField(max_length=300, blank=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)


