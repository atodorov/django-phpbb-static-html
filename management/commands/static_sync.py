import os
from phpbb_to_static import views
from phpbb_to_static.models import *
from django.core.files.base import ContentFile
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import AnonymousUser
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Sync the static HTML export from phpBB to default storage'
    can_import_settings = True

    def handle(self, *args, **options):
        generate_static_pages()


def _create_file(filename, contents):
    filename = filename.replace('//', '/')
    if not filename.startswith(default_storage.location):
        filename = os.path.join(default_storage.location, filename.lstrip("/"))

    default_storage.save(filename, ContentFile(contents))

def generate_static_pages():
    # dummy object to pass to views
    env = {
            'REQUEST_METHOD' : 'GET',
            'wsgi.input' : None,
        }
    request = WSGIRequest(env)
    request.user = AnonymousUser()

    # index view
    request.path = ''
    response = views.index(request)
    _create_file('index.html', response.content)

    # forums views
    for f in Forum.objects.filter(parent_id__gt=0):
        request.path = 'f/%d/' % f.pk
        response = views.forum(request, f.pk)
        _create_file('%s/index.html' % request.path, response.content)
        print "DONE", request.path

    # topics views
    for t in Topic.objects.all():
        latin_title = t.latin_title()
        request.path = 't/%d/%s/' % (t.pk, latin_title)
        response = views.topic(request, t.pk, latin_title)
        _create_file('%s/index.html' % request.path, response.content)
        print "DONE", request.path




