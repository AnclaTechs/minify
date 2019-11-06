from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Profile, User
from .forms import ProfileEditForm
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from nfunctions.models import Notification
from base.models import Posts


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, slug):
        profile = get_object_or_404(Profile, slug=slug)
        notification = Notification.objects.filter(user=request.user)
        notif_count = notification.count()
        notif_unread_count = Notification.objects.filter(user=request.user, read=False).count()
        posts = Posts.objects.filter(owner=profile).order_by("-created")[0:50]

        return render(
            request,
            'acctmang/profile_detail.html',
            context={
                'object': profile,
                'notifications': notification,
                'notification_count': notif_count,
                'unread': notif_unread_count,
                'posts': posts
            }
        )


class EditProfile(LoginRequiredMixin, View):
    def get(self, request, id, slug):
        profile_instance = get_object_or_404(Profile, user=request.user, slug=slug)
        form = ProfileEditForm(request.GET, instance=profile_instance)
        return render(
            request,
            "acctmang/edit_profile.html",
            {"form": form, "profile": profile_instance}

        )
    
    def post(self, request, id, slug):
        profile_instance = get_object_or_404(Profile, user=request.user, slug=slug)
        form = ProfileEditForm(request.POST, instance=profile_instance)
        if form.is_valid():
            profile_instance.firstname = form["firstname"].value()
            profile_instance.lastname = form["lastname"].value()
            profile_instance.location = form["location"].value()
            profile_instance.twitter = form["twitter"].value()
            profile_instance.instagram = form["instagram"].value()
            profile_instance.github = form["github"].value()
            profile_instance.website = form["website"].value()
            profile_instance.tstack = form["tstack"].value()
            profile_instance.bio = form["bio"].value()

            profile_instance.save(update_fields=[
                "firstname",
                "lastname",
                "location",
                "twitter",
                "instagram",
                "github",
                "website",
                "tstack",
                "bio"
            ])
            return redirect(reverse_lazy('user-profile', kwargs={'slug':slug}))