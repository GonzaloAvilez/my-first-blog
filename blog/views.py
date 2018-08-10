from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from . models import Post
from .forms import PostForm

from django.shortcuts import redirect
from .forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def post_list(request):
		posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        	return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
		post = Post.objects.get(pk=pk)
		 
def post_detail(request, pk): 
		post = get_object_or_404(Post, pk=pk) 
		return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

#create a view for register user

def register(request):
    context = RequestContext(request)
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response('blog/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)

#login
def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('blog/login.html', {}, context)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/blog/')