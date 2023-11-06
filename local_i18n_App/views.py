from .serializers import ListSerializer
from .models import List
from rest_framework import generics
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import render
from .models import Category, Post
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from rest_framework.response import Response
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import translation


def index(request):
    if request.user.is_authenticated:
        messages.success(request, _("authmessage {first} {last}").format(
            first=request.user.first_name, last=request.user.last_name), extra_tags="alert alert-success")
    else:
        messages.warning(request, _("anonmessage"),
                         extra_tags="alert alert-danger")

    # Get the language code from the request.
    language_code = request.LANGUAGE_CODE

    # Filter the posts by language code.
    posts = Post.objects.filter(translations__language_code=language_code)

    context = {'posts': posts}
    return render(request, 'index.html', context)

# do image upload here for rest api to json path


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Save the uploaded image file
            image_file = request.FILES.get('image', None)
            if image_file:
                post = serializer.instance
                post.image.save(image_file.name, image_file, save=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = MovieName.objects.all()
        serializer = MovieNameSerializer(movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieNameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def list_list(request):
    if request.method == 'GET':
        lists = List.objects.all()
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT',])
def settings_list(request):
    if request.method == 'GET':
        settings = SiteSettings.objects.all()

        # Dil ayarını isteğe göre güncelle
        if 'language' in request.GET:
            settings.language = request.GET['language']
            settings.save()

        serializer = SiteSettingsSerializer(settings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SiteSettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        settings = SiteSettings.objects.get()
        serializer = SiteSettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
