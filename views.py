from models import *
from django.conf import settings
from django.shortcuts import render

def index(request):
    context = {}

    for f in Forum.objects.filter(parent_id=0).exclude(pk__in=settings.PHPBB_SKIP_FORUMS):
        context[f.forum_id] = { 'f' : f, 'children' : []}
        for sf in Forum.objects.filter(parent_id=f.forum_id).exclude(pk__in=settings.PHPBB_SKIP_FORUMS):
            context[f.forum_id]['children'].append(sf)

    return render(request, 'index.html', {'forums' : context })

def forum(request, forum_id):
    context = []
    forum = Forum.objects.get(pk=forum_id)

    for t in Topic.objects.filter(forum_id=forum_id, topic_approved=True).order_by('-topic_time'):
        context.append(t)

    return render(request, 'forum.html', {'topics' : context, 'forum' : forum })

def topic(request, topic_id, subject):
    context = []
    topic = Topic.objects.get(pk=topic_id)

    for p in Post.objects.filter(topic_id=topic_id, post_approved=True).order_by('post_time'):
        try:
            user = User.objects.get(pk=p.poster_id)
        except:
            user = User(username=p.post_username)

        context.append((p, user))

    return render(request, 'topic.html', {'posts' : context, 'topic' : topic })

