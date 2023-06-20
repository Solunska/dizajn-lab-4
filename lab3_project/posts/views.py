from django.shortcuts import render
from .models import Post, Comment, UserProfile
from .forms import PostForm, BlockedUsersForm
from django.contrib.auth.models import User
from django.shortcuts import redirect


# Create your views here.

def posts_view(request):
    blocked_users = request.user.userprofile.blocked_users.all()
    posts = Post.objects.exclude(author__in=blocked_users).exclude(author=request.user)
    return render(request, 'posts.html', {'posts': posts})


def add_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    context = {"form": PostForm}
    return render(request, 'add.html', context=context)


def profile_view(request):
    user = request.user
    profile = user.userprofile
    posts = Post.objects.filter(author=user)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})


def blocked_users_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profiles = User.objects.exclude(id=request.user.id)
    blocked_users = user_profile.blocked_users.all()

    if request.method == 'POST':
        form = BlockedUsersForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile.blocked_users.set(form.cleaned_data['blocked_users'])
            return redirect('blockedUsers')
    else:
        initial_blocked_users = blocked_users.values_list('id', flat=True)
        form = BlockedUsersForm(instance=user_profile, initial={'blocked_users': initial_blocked_users})

    context = {
        'blocked_users': blocked_users,
        'user_profiles': user_profiles,
        'form': BlockedUsersForm
    }
    return render(request, 'blockedUsers.html', context=context)
