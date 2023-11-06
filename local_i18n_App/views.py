from .serializers import *
from rest_framework import generics
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import render
from .models import *
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


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
