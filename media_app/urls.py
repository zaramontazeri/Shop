from django.urls import path
from .views import *

urlpatterns = [
    path('image', ImageUploadView.as_view()),
    path('image_list/', ImageListAPIView.as_view()),
    path ('image_update/<int:pk>/',ImageUpdateAPIView.as_view()),
    path ('image_delete/<int:pk>/',ImageDeleteAPIView.as_view()),
    path ('image_detail/<int:pk>/',ImageDetailAPIView.as_view()),
    path ('image_thumbnail/',ImageListThumbNailAPIView.as_view()),

    path('file', FileUploadView.as_view()),
    path('file_list/', FileListAPIView.as_view()),
    path ('file_update/<int:pk>/',FileUpdateAPIView.as_view()),
    path ('file_delete/<int:pk>/',FileDeleteAPIView.as_view()),
    path ('file_detail/<int:pk>/',FileDetailAPIView.as_view()),

]