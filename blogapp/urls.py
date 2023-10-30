from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name="index"),
    # path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<str:category>', views.post_list, name='post_list_category'),
    path('posts/detail/<id>', views.posts_details, name='posts_detail'),
    path('ticket', views.ticket, name='ticket'),
    path('posts/<post_id>/comment', views.post_comment, name="post_comment"),
    # path('create_post',views.create_posts_view,name = "create__posts"),
    path('search', views.post_search, name="post_search"),
    path('profile', views.profile, name="profile"),
    path('profile/create_post', views.create_post, name="create_post"),
    path('profile/create_post/<post_id>', views.edit_post, name="edit_post"),
    path('profile/delete_post/<post_id>', views.delete_post, name="delete_post"),
    path('profile/delete_image/<image_id>', views.delete_image, name="delete_image"),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', views.log_out, name="logout"),
    path('change-password', auth_views.PasswordChangeView.as_view(success_url='change-password-done'), name='change'
                                                                                                            '_password'),
    path('change-password-done', auth_views.PasswordChangeDoneView.as_view(), name='change_password_done'),
    # reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password'
                                                                                                     '-reset/complete'), name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('register/', views.register, name='register'),
    path('register/edit', views.edit_account, name='edit_account'),
    path('profile/user', views.user, name='user'),
    path('profile/post_comment/<post_id>', views.post_comment_user, name='post_comment_user')
]
