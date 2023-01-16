from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponsePermanentRedirect
from django.views.generic.base import View, TemplateView

from .models import Post
from .strings import template_strings
from .transforms import render_post_preview


class HomePage(TemplateView):
    template_name = "main.html"
    http_method_names = ["get", "head", "options"]

    def get_context_data(self, **kwargs):
        context = template_strings()
        context.update(super().get_context_data(**kwargs))
        recent_posts = Post.objects.all().order_by("-save_time")#[:3]
        context["latest_posts"] = [render_post_preview(p) for p in recent_posts]
        return context


class ProfilePic(View):

    def get(self, request, *args, **kwargs):
        return HttpResponsePermanentRedirect(staticfiles_storage.url('profile.jpg'))
