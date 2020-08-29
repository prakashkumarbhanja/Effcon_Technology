from django.urls import path
from django.views.generic.base import RedirectView
from social import views

# urlpatterns = [     #1:14 no:-16
#     path('home/', views.HomeView.as_view()),
#     path('about/', views.AboutView.as_view()),
#     path('contact/', views.ContactView.as_view()),
#     path('profile/edit/<int:pk>', views.ProfileUpdateView.as_view(success_url='/social/home')),
#     path('mypost/create/', views.MyPostCreate.as_view(success_url='/social/home')),
#     path('mypost/', views.MyPostListView.as_view()),
#     path('mypost/<int:id>', views.MyPostDetailView.as_view()),
#
#     path('follow/<int:pk>', views.follow, name='follow'),
#
#     path('', RedirectView.as_view(url="home/")),
#
# ]

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contactus/', views.ContactView.as_view(), name='contactus'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('createuser/', views.createuser, name='create_user'),

    path('edit/<int:id>', views.MyProfileUpdateView.as_view(success_url = "/social/home"), name='Update_Profile'),

    path('mypost/create/', views.MyPostCreate.as_view(success_url='/social/mypost/list'), name='createmypost'),
    path('mypost/list/', views.post_list, name='mypostlist'),
    # path('mypost/detail/<int:id>', views.MyPostDetailView.as_view(), name='mypostDetail'),
    path('mypost/detail/<int:id>', views.post_detail, name='mypostDetail'),
    path('mypost/delete/<int:id>', views.mypostdelete, name='mypostdelete'),
    path('mypost/mypostsearch', views.mypostsearch, name='mypostsearch'),

    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('myprofile/update/<int:pk>', views.MyProfileUpdateView.as_view(), name='myprofileupdate'),
    path('myprofile/<int:id>', views.myprofiledetailview, name='myprofiledetail'),

    path('follow/<int:id>', views.follow, name='follow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),

    path('FollowedPost/', views.FollowedPost.as_view(), name='FollowedPost'),

    path('post/like/<int:id>', views.postlike, name='postlike'),
    path('post/dislike/<int:id>', views.postdislike, name='postdislike'),


    path('', RedirectView.as_view(url="home/")),

]