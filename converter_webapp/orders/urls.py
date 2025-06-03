from django.urls import path

from . import views


urlpatterns = [
    path('upload/', views.UploadExelView.as_view(), name='upload'),
    path('albums/', views.AlbumListView.as_view(), name='albums'),
]
