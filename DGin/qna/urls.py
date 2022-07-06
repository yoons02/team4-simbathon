"""DGin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

app_name = "qna"
urlpatterns = [
    path('majorlist/', majorList, name="majorList"),
    path('nonmajorlist/', nonmajorList, name="nonmajorList"),
    
    path('<int:id>', detail, name="detail"),
    path('major_new/', major_new, name="major_new"),
    path('nonmajor_new/', nonmajor_new, name="nonmajor_new"),
    path('major_create/', major_create, name="major_create"),
    path('nonmajor_create/', nonmajor_create, name="nonmajor_create"),
    path('edit/<int:id>', edit, name="edit"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:id>', delete, name="delete"),
    path('<str:question_id>/create_answer/', create_answer, name="create_answer"),
    path('<str:question_id>/edit_answer/<str:answer_id>', edit_answer, name="edit_answer"),
    path('<str:question_id>/update_answer/<str:answer_id>', update_answer, name="update_answer"),
    path('<str:question_id>/delete_answer/<str:answer_id>', delete_answer, name="delete_answer"),

    path('<int:id>/likes/', likes, name="likes"),
    path('<int:question_id>/select/<int:answer_id>', select, name="select"),
    path('search/', search, name='search'),
]
