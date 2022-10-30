from django.views.generic.base import TemplateView

from .models import Post
from .strings import template_strings
from .transforms import render_post_preview


class HomePage(TemplateView):
    template_name = "main.html"
    http_method_names = ["get", "head", "options"]

    def get_context_data(self, **kwargs):
        context = template_strings() | super().get_context_data(**kwargs)
        recent_posts = Post.objects.all().order_by("-save_time")#[:3]
        context["latest_posts"] = [render_post_preview(p) for p in recent_posts]
        return context

