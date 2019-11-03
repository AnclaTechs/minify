from django.contrib import admin
from .models import QuestionTags, Questions, Posts, QueComment, Like
from .models import QueAnswer, QueAnswerComment, Vote, PostsCommentary
from .models import Note

#
admin.site.register(Note)
admin.site.register(QuestionTags)
admin.site.register(Questions)
admin.site.register(Posts)
admin.site.register(QueComment)
admin.site.register(QueAnswer)
admin.site.register(Vote)
admin.site.register(QueAnswerComment)
admin.site.register(Like)
admin.site.register(PostsCommentary)
