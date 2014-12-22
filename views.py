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

    for t in Topic.objects.filter(forum_id=forum_id):
        context.append(t)

    return render(request, 'forum.html', {'topics' : context })

def topic(request, topic_id):
    context = []

    for p in Posts.objects.filter(topic_id=topic_id):
        context.append(p)

    return render(request, 'topic.html', {'posts' : context })
