from django.shortcuts import render
from django.http import HttpResponse

def post_list(request):
    return HttpResponse("Blog post list")

def post_detail(request, post_id):
    return HttpResponse(f"Blog post detail for post {post_id}")
