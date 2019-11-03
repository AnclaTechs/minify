from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Profile, User
from .forms import ProfileEditForm
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin



class ProfileView(LoginRequiredMixin, generic.DetailView):
    model =Profile

    def profile_page(request, slug):
        profile = get_object_or_404(Profile, slug=slug)

        return render(
            request,
            'acctmang/profile.html',
            context={'profile': profile}
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