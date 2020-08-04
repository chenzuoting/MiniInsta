from annoying.decorators import ajax_request
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.models import InstaUser, Post, Like, UserConnection, Comment
from Insta.forms import CustomUserCreationForm

# Create your views here.

class HelloWorld(TemplateView):
    template_name = 'helloworld.html'

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    login_url = 'login'

    # Only show posts from followings
    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
        if liked:
            data['liked'] = 1
        else:
            data['liked'] = 0
        return data

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'image']
    login_url = 'login'

    # Manually set author here
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']
    login_url = 'login'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    #cannot use reverse here, we are trying to redirect during delete process, which is invalid
    #with reverse_lazy, we are redirecting and let delete running in the back
    success_url = reverse_lazy("home")
    login_url = 'login'

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

class UserProfileView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'user_profile.html'
    login_url = 'login'

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'edit_profile.html'
    fields = ['username', 'profile_pic']
    login_url = 'login' 

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    # def get_queryset(self):
    #     return Post.objects.all().order_by('-posted_on')[:20]

# Annotation: this function is to response ajax request, no need to render to a template
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0
    # if Like.objects.filter(post=post, user=request.user).exists():
    #     like = Like.objects.get(post=post, user=request.user)
    #     like.delete()
    #     result = 0
    # else:
    #     like = Like(post=post, user=request.user)
    #     like.save()
    #     result = 1

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }
    
@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }