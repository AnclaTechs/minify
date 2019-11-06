from django.urls import path, re_path
from .views import index, home, new_question, get_questions
from .views import QuestionDetailView, answer_question, vote_answer
from .views import make_post, PostView, like_post, pass_commentary
from .views import add_notes, get_notes, view_note, EditNote, shared_note
from .views import note_share_user_confirmation, share_note, save_sharednote_copy
urlpatterns = [
    path("", index, name="home"),
    path("general/", home, name="generic"),
    path("newQuestion/", new_question, name="new_question"),
    path("get_questions/", get_questions, name="get_question"),
    path("question/<int:pk>/<slug:title>",
         QuestionDetailView.as_view(), name="question-detail"),
    path("question/give-answer/<int:pk>/page",
         answer_question, name='answer-question'),
    path("answer/vote", vote_answer, name="answer-vote"),
    #
    path("makepost", make_post, name="makepost" ),
    path("post/<int:pk>/<slug:username>", PostView.as_view(), name="post-detail" ),
    #
    path("likepost", like_post),
    path("passcomment", pass_commentary),
    #
    path("addnote", add_notes, name="add-note"),
    path("getnote", get_notes, name="get-note"),
    path("note/<int:pk>/<slug:slug>", view_note, name="view-note"),
    path("editnote/<int:pk>/<slug:slug>", EditNote.as_view(), name="edit-note"),
    path("sharednote/<int:pk>/<slug:slug>", shared_note, name="shared-note"),
    path("minify-actions/confirm-user-to-share", note_share_user_confirmation),
    path("minify-actions/share-note", share_note),
    path("minify-actions/save-shared-note", save_sharednote_copy),    






]
