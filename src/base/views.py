from django.shortcuts import render, redirect, get_object_or_404, redirect
#from django.urls import reverse
from .forms import SignupForm, NoteForm
from .models import Posts, Questions, QueAnswer, Vote, Like, Note
from .models import PostsCommentary
from acctmang.models import User
from django.views import generic, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import JsonResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.text import slugify
import timeago
from datetime import datetime
import pytz
from nfunctions.models import UrlHit, HitCount, Notification
from minify.mailer import Mailer
mail = Mailer()
from copy import deepcopy


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hit_count(request):
    if not request.session.session_key:
        request.session.save()
    s_key = request.session.session_key
    ip = get_client_ip(request)
    url, url_created = UrlHit.objects.get_or_create(url=request.path)

    if url_created:
        track, created = HitCount.objects.get_or_create(url_hits=url, ip=ip, session=s_key)
        if created:
            url.increase()
            request.session[ip] = ip
            request.session[request.path] = request.path

    else:
        if ip and request.path not in request.session:
            track, created = HitCount.objects.get_or_create(url_hits=url, ip=ip, session=s_key)
            if created:
                url.increase()
                request.session[ip] = ip
                request.session[request.path] = request.path
    
    return url.hits

def index(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            #POST is redirected to 'account-signup' on template
            pass
    else:
        form = SignupForm()

    context = {
        "form": form
    }
    return render(
        request,
        "base_landing.html",
        context
    )


def home(request):
    post = Posts.objects.all().order_by("-created")
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 10)
    try:
        post_em = paginator.page(page)
    except PageNotAnInteger:
        post_em = paginator.page(1)
    except EmptyPage:
        post_em = paginator.page(paginator.num_pages)

    return render(
        request,
        'home.html',
        context={ "post_em": post_em }
    )


@login_required
def new_question(request):
    if request.method == "POST" and request.is_ajax:
        user = request.user
        title = request.POST.get("title")
        question = request.POST.get("question")
        slug_prep = str(title).replace(" ", "-")
        slug = slugify(slug_prep)
        # try and catch here
        Questions.objects.create(
            owner=user, title=title, body=question, slug=slug)
        payload = {"url": "/general/"}
        payload = json.dumps(payload)
        return JsonResponse(json.loads(payload), safe=False)

    return render(
        request,
        "question.html"
    )


def get_questions(request):
    if request.is_ajax:
        object_length = Questions.objects.all().count()
        query = Questions.objects.all().order_by("-created")[0: 50]
        questions_list = []
        for item in query:
            question = {}
            question["id"] = item.id
            question["title"] = item.title
            question["slug"] = item.slug
            question["answersCount"] = item.queanswers.count()
            question["viewsCount"] = item.views
            creation_date = item.created
            last_modified = item.modified
            lagos = pytz.timezone('Africa/Lagos')
            if last_modified < creation_date:
                time_ago = timeago.format(
                    last_modified, datetime.now(lagos))
                question["time"] = time_ago
            else:
                time_ago = timeago.format(
                    creation_date, datetime.now(lagos))
                question["time"] = time_ago
            # view_no
            questions_list.append(question)

        payload = {"questionLog": questions_list, "total": object_length}
        payload = json.dumps(payload)
        return JsonResponse(json.loads(payload), safe=False)


class QuestionDetailView(View):
    #model = Questions

    def get(self, request, pk, title):
        unique_page_view = hit_count(request)
        question = get_object_or_404(Questions, pk=pk)#skip slug-title
        question.views = unique_page_view
        question.save(update_fields=["views"])
        return render(
            request,
            'base/questions_detail.html',
            context={'object': question}

        )


@login_required
def answer_question(request, pk):
    if request.method == "POST" and request.is_ajax:
        questionID = request.POST.get("questionID")
        answer = request.POST.get("answer")
        user = request.user
        question_inView = Questions.objects.get(id=questionID)
        #
        QueAnswer.objects.create(
            question=question_inView, author=user, body=answer)
        url = "/question/{}/{}".format(questionID, question_inView.slug)
        payload = {"url": url}
        payload = json.dumps(payload)
        return JsonResponse(json.loads(payload), safe=False)

    question = get_object_or_404(Questions, pk=pk)
    return render(
        request,
        'base/answer_question.html',
        context={'question': question}
    )

def vote_answer(request):
    if request.method == "POST" and request.is_ajax:
        if request.user.is_authenticated:
            user = request.user.id
            answer_id = request.POST.get("answerId")
            action = request.POST.get("action")
            answer = QueAnswer.objects.get(id=answer_id)
            vote = Vote.objects.get(answer=answer)
            if action == "upvote":
                if vote.users_vote[str(user)] ==  "downvote":
                    vote.users_vote[int(user)] =  "upvote"
                    vote.upvote += 1
                    vote.downvote -= 1
                    vote.save(update_fields=[
                        "users_vote",
                        "upvote",
                        "downvote"
                    ])

                elif vote.users_vote[str(user)] ==  "upvote":
                    pass
                
                else:
                    vote.users_vote[int(user)] =  "upvote"
                    vote.upvote += 1
                    vote.save(update_fields=[
                        "users_vote",
                        "upvote",
                    ])

            elif action == "downvote":
                if vote.users_vote[str(user)] == "upvote":
                    vote.users_vote[int(user)] = "downvote"
                    vote.downvote += 1
                    vote.upvote -= 1
                    vote.save(update_fields=[
                        "users_vote",
                        "downvote",
                        "upvote"

                    ])

                elif vote.users_vote[str(user)] == "downvote":
                    pass

                else:
                    vote.users_vote[int(user)] = "downvote"
                    vote.downvote += 1
                    vote.save(update_fields=[
                        "users_vote",
                        "downvote",

                    ])


            payload = {"status": "success"}
            payload = json.dumps(payload)

            return JsonResponse(json.loads(payload), safe=False)
        else:
            payload = {"url": "/accounts/login/"}
            payload = json.dumps(payload)

            return JsonResponse(json.loads(payload), safe=False)


#POSTS
def make_post(request):
    assert request.user.is_authenticated
    if request.method == "POST" and request.is_ajax:
        user = request.user.profile
        username = request.user.username
        post_content = request.POST.get("postContent")
        new_post = Posts.objects.create(owner=user, body=post_content)
        post_link = '/post/{}/{}'.format(new_post.id, username )
        payload = {"url": post_link }
        payload = json.dumps(payload)

        return JsonResponse(json.loads(payload), safe=False)


class PostView(generic.DetailView):
    model = Posts

    def get_post_view(request, primary_key, username):
        post = get_object_or_404(Posts, pk=primary_key)

        return render(
            request,
            context={'post': post}
        )

    

def like_post(request):
    if request.method == "POST" and request.is_ajax:
        if request.user.is_authenticated:
            post_id = request.POST.get("id")
            post_in_view = Posts.objects.get(id=post_id)
            user = request.user
            Like.objects.create(user=user, post=post_in_view)

            payload = {"status": "success"}
            payload = json.dumps(payload)

            return JsonResponse(json.loads(payload), safe=False)

        else:
            payload = {"url": "/accounts/login/"}
            payload = json.dumps(payload)

            return JsonResponse(json.loads(payload), safe=False)


def pass_commentary(request):
    assert request.user.is_authenticated
    if request.method == "POST" and request.is_ajax:
        user = request.user.profile
        username = request.user.username
        post_id = request.POST.get("id")
        post_in_view = Posts.objects.get(id=post_id)
        comment = request.POST.get("postContent")
        PostsCommentary.objects.create(owner=user, post=post_in_view, body=comment)
        payload = {"status": "success"}
        payload = json.dumps(payload)

        return JsonResponse(json.loads(payload), safe=False)


#MINIFYNOTES
@login_required
def add_notes(request):
    form = NoteForm(request.POST)
    if form.is_valid():
        title = form["title"].value()
        slug_prep = str(title).replace(" ", "-")
        slug = slugify(slug_prep)
        notetype = form["notetype"].value()
        body = form["note"].value()
        links = form["links"].value()
        public = form["public"].value()
        new_note = Note.objects.create(owner=request.user, title=title, slug=slug, notetype=notetype, note=body, links=links, public=public)

        return HttpResponseRedirect('/general/')
    else:
        form = NoteForm()

    context = {
        "form": form
    }
    return render(
        request,
        "notes/add_note.html",
        context
    )

@login_required
def get_notes(request):
    try:
        assert request.user.is_authenticated
    except AssertionError:
        payload = {"queryStatus": "failed"}
        payload = json.dumps(payload)

        return JsonResponse(json.loads(payload), safe=False)

    if request.method == "GET" and request.is_ajax:
        user = request.user
        query = Note.objects.filter(owner=user).order_by("-modified")
        query_list = []
        for item in query:
            note = {}
            note["id"] = item.id
            note["title"] = item.title
            note["slug"] = item.slug
            note["body"] = item.note[0:200]
            note["links"] = item.links
            if item.modified == None:
                note["modified"] = item.created.isoformat()
            else:
                note["modified"] = item.modified.isoformat()
            query_list.append(note)
        
        payload = {"mininotes": query_list}
        payload = json.dumps(payload)

        return JsonResponse(json.loads(payload), safe=False)




@login_required
def edit_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, instance=request.user)

        if form.is_valid():
            note = note.save(commit=False)
            note.save()
            return HttpResponseRedirect('/general/')
        else:
            return render(
                request,
                "edit_note.html",
                {"form", form
            })
    else:
        form = NoteForm(instance=request.user)
        context = {'form': form}
        return request(
            request,
            "edit_note.html",
            context
        )

@login_required
def view_note(request, pk, slug):
    note_instance = get_object_or_404(Note, owner=request.user, id=pk) #skip slug
    context= {"note": note_instance}
    return render(
        request,
        "notes/view_note.html",
        context
    )


class EditNote(View):
    def get(self, request, pk, slug):
        note_instance = get_object_or_404(Note, owner=request.user, id=pk) #skip slug
        form = NoteForm(request.GET, instance=note_instance)
        return render(
            request,
            "notes/edit_note.html",
            {"form": form, "note": note_instance}
        )

    def post(self, request, pk, slug):
        note_instance = get_object_or_404(Note, owner=request.user, id=pk) #skip slug
        form = NoteForm(request.POST)
        if form.is_valid():
            note_instance.title = title = form["title"].value()
            slug_prep = str(title).replace(" ", "-")
            note_instance.slug = slugify(slug_prep)
            note_instance.notetype = form["notetype"].value()
            note_instance.note = form["note"].value()
            note_instance.links = form["links"].value()
            note_instance.public = form["public"].value()
            note_instance.modified = datetime.now()

            note_instance.save(update_fields=[
                "title",
                "slug",
                "notetype",
                "note",
                "links",
                "public",
                "modified",
            ])
            return redirect(reverse_lazy('view-note', kwargs={'pk':pk, 'slug': note_instance.slug}))


@login_required
def shared_note(request, pk, slug):
    note = get_object_or_404(Note, pk=pk)
    #check owner permitted viewers
    if note.permitted_viewers != {}:
        if request.user.id in note.permitted_viewers["viewers"]:
            note_action = "/sharednote/{}/{}".format(note.id, note.slug)
            try:
                notification = Notification.objects.get(user=request.user, action=note_action)
                notification.read = True
                notification.save(update_fields=["read"])        
            except ObjectDoesNotExist:
                pass
            return render(
                request,
                "notes/shared_note.html",
                {"object": note}
            )
        else:
            return render(
                request,
                "notes/shared_note.html",
                {"access": "empty"}
            )
    else:
        return render(
            request,
            "notes/shared_note.html",
            {"access": "empty"}
        )

def note_share_user_confirmation(request):
    try:
        assert request.user.is_authenticated
    except AssertionError:
        payload = {"queryStatus": "failed"}
        payload = json.dumps(payload)

        return JsonResponse(json.loads(payload), safe=False)

    if request.method == "POST" and request.is_ajax:
        username_email = request.POST.get("usernameEmail")
        #note_id = request.POST.get("noteID")
        #user = request.user
        #note = get_object_or_404(Note, owner=user, pk=note_id)
        if "@" in username_email:
            try:
                user = User.objects.get(email=username_email)
            except ObjectDoesNotExist:
                payload = {"queryStatus": "failed"}
                payload = json.dumps(payload)
                return JsonResponse(json.loads(payload), safe=False)
        else:
            try:
                user = User.objects.get(username=username_email)
            except ObjectDoesNotExist:
                payload = {"queryStatus": "failed"}
                payload = json.dumps(payload)
                return JsonResponse(json.loads(payload), safe=False)

        if user:
            username = user.get_username()
            payload = {"queryStatus": "success", "username": username}
            payload = json.dumps(payload)
            return JsonResponse(json.loads(payload), safe=False)



def share_note(request):
    try:
        assert request.user.is_authenticated
    except AssertionError:
        payload = {"requestStatus": "failed"}
        payload = json.dumps(payload)

        return JsonResponse(json.loads(payload), safe=False)

    if request.method == "POST" and request.is_ajax:
        username_email = request.POST.get("usernameEmail")
        note_id = request.POST.get("noteId")
        user = request.user
        note = get_object_or_404(Note, owner=user, pk=note_id)

        if "@" in username_email:
            try:
                receiver = User.objects.get(email=username_email)
            except ObjectDoesNotExist:
                payload = {"requestStatus": "failed"}
                payload = json.dumps(payload)
                return JsonResponse(json.loads(payload), safe=False)
        else:
            try:
                receiver = User.objects.get(username=username_email)
            except ObjectDoesNotExist:
                payload = {"requestStatus": "failed"}
                payload = json.dumps(payload)
                return JsonResponse(json.loads(payload), safe=False)
        
        if note and user:
            if note.permitted_viewers == {}:
                note.permitted_viewers["viewers"] =  []
                note.permitted_viewers["viewers"].append(receiver.id)
                note.save(update_fields=["permitted_viewers"])
                #
                notification_message = "@{} sent you a note".format(user.get_username())
                notification_action = "sharednote/{}/{}".format(note.id, note.slug)
                Notification().add_notfication(receiver, notification_message, notification_action)
                #
                mail.send_messages(
                    subject="Notification from Minify",
                    template="gen_emails/noteshare_notification.html",
                    context={'sender': user.get_username(), "link": notification_action},
                    to_emails=[receiver.email]
                )
                #
                payload = {"requestStatus": "success"}
                payload = json.dumps(payload)
                return JsonResponse(json.loads(payload), safe=False)

            else:
                if user in note.permitted_viewers:
                    #pass
                    payload = {"requestStatus": "success"}
                    payload = json.dumps(payload)
                    return JsonResponse(json.loads(payload), safe=False)
                else:
                    note.permitted_viewers["viewers"].append(receiver.id)
                    note.save(update_fields=["permitted_viewers"])
                    #
                    notification_message = "@{} sent you a note".format(user.get_username())
                    notification_action = "sharednote/{}/{}".format(note.id, note.slug)
                    Notification().add_notfication(receiver, notification_message, notification_action)
                    #
                    mail.send_messages(
                        subject="Notification from Minify",
                        template="gen_emails/noteshare_notification.html",
                        context={'sender': user.get_username(), "link": notification_action},
                        to_emails=[receiver.email]
                    )
                    #
                    payload = {"requestStatus": "success"}
                    payload = json.dumps(payload)
                    return JsonResponse(json.loads(payload), safe=False)
        else:
            payload = {"requestStatus": "failed", "message": "Error approving rights"}
            payload = json.dumps(payload)
            return JsonResponse(json.loads(payload), safe=False)


def save_sharednote_copy(request):
    try:
        assert request.user.is_authenticated
    except AssertionError:
        payload = {"requestStatus": "failed"}
        payload = json.dumps(payload)

        return JsonResponse(json.loads(payload), safe=False)

    if request.method == "POST" and request.is_ajax:
        pk = request.POST.get("id")
        note = get_object_or_404(Note, pk=pk)
        #check owner permitted viewers
        if note.permitted_viewers != {}:
            if request.user.id in note.permitted_viewers["viewers"]:
                new_instance = deepcopy(note)
                new_instance.id = None
                new_instance.owner = request.user
                new_instance.save()
                #
                payload = {"requestStatus": "success", "url": "/general/"}
                payload = json.dumps(payload)
                return JsonResponse(json.loads(payload), safe=False)


            else:
                payload = {"requestStatus": "failed"}
                payload = json.dumps(payload)
                return JsonResponse(json.loads(payload), safe=False)

        else:
            payload = {"requestStatus": "failed"}
            payload = json.dumps(payload)
            return JsonResponse(json.loads(payload), safe=False)





def handler404(request,
	exception,
	template_name="404.html",
	):
	response = render_to_response("404.html")
	response.status_code = 404
	return response

def handler500(request,
	template_name="500.html",
	):
	response = render_to_response("500.html")
	response.status_code = 500
	return response