from django.views.generic import TemplateView
from posts.models import Post
import datetime as dt


class IndexPageView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(only_for_group=False)
        return context


def get_current_year(request):
    return {
        'year': dt.datetime.now().year
    }

