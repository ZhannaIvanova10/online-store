from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F

from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    """Контроллер для списка блоговых записей."""
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        """Возвращает только опубликованные записи."""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogPostDetailView(DetailView):
    """Контроллер для детального просмотра блоговой записи."""
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def get_object(self, queryset=None):
        """Получает объект и увеличивает счетчик просмотров."""
        obj = super().get_object(queryset)
        obj.views_count = F('views_count') + 1
        BlogPost.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db()
        return obj


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания новой блоговой записи."""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования блоговой записи."""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_success_url(self):
        """После успешного редактирования перенаправляем на статью."""
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления блоговой записи."""
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
