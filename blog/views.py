from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from .serializers import BlogSerializer
# Create your views here.

class BlogListCreateView(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.filter(author=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        title = data.get('title')
        content = data.get('content')
        author = request.user
        blog = Blog.objects.create(title=title, content=content, author=author)
        return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)

class BlogRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        title = data.get('title',instance.title)
        content = data.get('content',instance.content)
        
        instance.title = title
        instance.content = content
        instance.save()
        
        return Response(BlogSerializer(instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


