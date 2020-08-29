from pyexpat.errors import messages

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import MyProfile, MyPost, PostComment, PostLike, FollowUser
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from .forms import LoginForm, CreateUserForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.

class HomeView(TemplateView):
    template_name = 'social/home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        print(self.request.user)
        try:
            context['myprofile'] = MyProfile.objects.filter(user=self.request.user)
        except:
            pass
        return context


class AboutView(TemplateView):
    template_name = 'social/about.html'


class ContactView(TemplateView):
    template_name = 'social/contact.html'



def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(redirect_to='/social/home')

    context = {"form": form}
    template = 'social/login.html'
    return render(request, template, context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/social/home')


def createuser(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        create_user = User.objects.create(username=username, email=email, password=password)
        create_user.save()
        return HttpResponseRedirect(redirect_to='/social/login')
    # else:
    #     return HttpResponse("Form is not valid")

    context = {'form': form}
    template = 'social/create-user.html'
    return render(request,template, context)


class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age", "address", "status", "gender", "phone_no", "description", "pic"]
    success_url = "/social/home"


class MyPostCreate(CreateView):
    model = MyPost
    fields = ['subject', 'msg', 'pic']
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def post_list(request):
   qs =  MyPost.objects.filter(Q(uploaded_by=request.user.myprofile))
   context = {"mypost_list": qs}

   return render(request, 'social/mypost_list.html', context)


def post_detail(request, id): #1:22 16
        qs = MyPost.objects.get(id=id)
        print(qs)
        context = {"mypost": qs}
        return render(request, 'social/mypost_detail.html', context)


def mypostdelete(request,id):
    del_obj = MyPost.objects.get(id=id)
    print("The delete id", del_obj.id)
    if request.method == "POST":
        del_obj.delete()
        return HttpResponseRedirect(redirect_to='/social/mypost/list')
    context = {"obj": del_obj}
    template = 'social/mypost_delete.html'
    return render(request, template, context)


def mypostsearch(request):
    try:
        si = request.POST.get('si')
    except:
        si = None
    if si:
        mypost = MyPost.objects.filter(Q(uploaded_by=request.user.myprofile)|Q(subject__icontains=si)|Q(msg__icontains=si))
        context = {"mypost": mypost}
    else:
        raise Http404
    return render(request, 'social/mypost_list.html', context)


class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        profList = MyProfile.objects.filter(Q(name__icontains = si) | Q(address__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si)).order_by("-id");
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile = p1,followed_by=self.request.user.myprofile)
            if ob:
                p1.followed = True
        return profList


def myprofiledetailview(request, id):
    try:
        myprofile = MyProfile.objects.get(id=id)
    except:
        return HttpResponse('Id does not exists')
    context = {'myprofile':myprofile}
    template = 'social/myprofile_detail.html'
    return render(request, template, context)


def follow(request, id):
    user = MyProfile.objects.get(id=id)
    follow = FollowUser.objects.create(profile= user,followed_by=request.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def unfollow(request, id):
    user = MyProfile.objects.get(id=id)
    FollowUser.objects.filter(profile=user, followed_by=request.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile")


class FollowedPost(TemplateView):
    template_name = 'social/followedpost.html'
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followList = FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        print(followList)
        followList2=[]
        for e in followList:
            print(e)
            followList2.append(e.profile)
        postslist = MyPost.objects.filter(uploaded_by__in=followList2)
        for p1 in postslist:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True
            objlist = PostLike.objects.filter(post=p1)
            p1.likedno = objlist.count()
        context['mypost_list'] = postslist
        return context

def postlike(request,id):
    post = MyPost.objects.get(id=id)
    PostLike.objects.create(post=post, liked_by=request.user.myprofile)
    return HttpResponseRedirect('/social/FollowedPost')

def postdislike(request, id):
    post = MyPost.objects.get(id=id)
    PostLike.objects.create(post=post, liked_by=request.user.myprofile).delete()
    return HttpResponseRedirect('/social/FollowedPost')