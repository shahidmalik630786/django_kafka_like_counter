from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from .models import Post
from kafka_producer import send_like_event

def post_like(request, post_id):
    send_like_event(post_id)
    # post = get_object_or_404(Post, id=post_id)
    # post.likes += 1
    # post.save()
    return JsonResponse({
        "status": True,
        "message": "Like incremented"
    })
