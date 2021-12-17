from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('logReg/', views.logReg),
    path('login/', views.login),
    path('reg/', views.register),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout),
    path('addNote/', views.addNote),
    path('createNote/', views.createNote),
    path('note/<int:note_id>/like/', views.likeNote),
    path('note/<int:note_id>/view/', views.viewNote),
    path('note/<int:note_id>/edit/', views.editNote),
    path('note/<int:note_id>/update', views.updateNote),
    path('note/<int:note_id>/upload/', views.uploadNote),
    path('user/<int:user_id>/viewProfile/', views.viewProfile),
    path('user/<int:user_id>/updateUser/', views.updateUser),
    path('user/<int:user_id>/updateDiscord/', views.updateDiscord),
    path('user/<int:user_id>/updateProfileImg/', views.updateImage),
    path('theAdmin/', views.theAdmin),
    path('theAdmin/allUsers/', views.adminAllUsers),
    path('theAdmin/allPosts/', views.adminAllPosts),
    path('theAdmin/comment/<int:note_id>/add/', views.adminAddComment),
    path('theAdmin/comment/<int:note_id>/create/', views.adminMakeComment),
    path('theAdmin/comment/<int:note_id>/view/', views.adminViewComment),
    path('theAdmin/note/<int:note_id>/edit/', views.adminEditNote),
    path('theAdmin/note/<int:note_id>/update/', views.adminUpdateNote),
    path('theAdmin/note/<int:note_id>/delete/', views.adminDeleteNote),
    path('theAdmin/<int:user_id>/makeAdmin/', views.makeAdmin),
    path('theAdmin/<int:user_id>/delete/', views.adminDeleteUser),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)