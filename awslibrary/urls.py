"""awslibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from library import views

urlpatterns = [
    path("", views.mybooks, name="mybooks"),
    path("books/", views.allbooks, name="allbooks"),
    path("newbook/", views.NewBook.as_view(), name="newbook"),
    path("books/<int:id>/", views.book, name="book"),
    path("addbook/<int:id>", views.addbook, name='addbook'),
    path("delbook/<int:id>", views.delbook, name='delbook'),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register', views.register, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
