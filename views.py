from models import *
from django.shortcuts import render

def index(request):
    context = {}

    for f in Forum.objects.filter(parent_id=0):
        context[f.forum_id] = { 'f' : f, 'children' : []}
        for sf in Forum.objects.filter(parent_id=f.forum_id):
            context[f.forum_id]['children'].append(sf)

    return render(request, 'index.html', {'forums' : context })

def forum(request, forum_id):
    context = []
    forum = Forum.objects.get(pk=forum_id)

    for t in Topic.objects.filter(forum_id=forum_id).order_by('-topic_time'):
        context.append(t)

    return render(request, 'forum.html', {'topics' : context, 'forum' : forum })

def topic(request, topic_id, subject):
    context = []
    topic = Topic.objects.get(pk=topic_id)

    for p in Post.objects.filter(topic_id=topic_id).order_by('post_time'):
        user = User.objects.get(pk=p.poster_id)
        context.append((p, user))

    return render(request, 'topic.html', {'posts' : context, 'topic' : topic })
