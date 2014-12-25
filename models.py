# -*- coding: utf-8 -*-

import hashlib
import string
from datetime import datetime
from django.db import models
from django.conf import settings

class Forum(models.Model):
    forum_id     = models.BigIntegerField(primary_key=True)
    parent_id    = models.BigIntegerField()
    left_id      = models.BigIntegerField()
    right_id     = models.BigIntegerField()
    forum_name   = models.CharField(max_length = 255)
    forum_desc   = models.TextField()
    forum_posts  = models.BigIntegerField()
    forum_topics = models.BigIntegerField()

    def __unicode__(self):
        return "(%d) %s" % (self.pk, self.forum_name)

    class Meta:
        managed = False
        db_table = "%s_forums" % settings.PHPBB_TABLE_PREFIX

class Topic(models.Model):
    topic_id = models.BigIntegerField(primary_key=True)
    forum_id = models.BigIntegerField()
    topic_title = models.CharField(max_length=255)
    topic_time = models.BigIntegerField() # this is a Unix timestamp, how stupid
    topic_views   = models.BigIntegerField()
    topic_replies = models.BigIntegerField()

# these can be 0, 1 and 2 but we don't need them probably
#    topic_status = tinyint(3) NOT NULL DEFAULT '0',
#    topic_type = tinyint(3) NOT NULL DEFAULT '0',

    topic_first_post_id = models.BigIntegerField()
    topic_first_poster_name = models.CharField(max_length=255)

    topic_last_post_id = models.BigIntegerField()
    topic_last_poster_name = models.CharField(max_length=255)


    def __unicode__(self):
        return "(%d) %s" % (self.pk, self.topic_title)

    def datetime(self):
        return datetime.fromtimestamp(self.topic_time)

    def latin_title(self):
        title = self.topic_title.lower().strip().replace("\n", "").replace("\r", "")
        translate_map = {
            u"а" : "a",
            u"б" : "b",
            u"в" : "v",
            u"г" : "g",
            u"д" : "d",
            u"е" : "e",
            u"ж" : "zh",
            u"з" : "z",
            u"и" : "i",
            u"й" : "i",
            u"к" : "k",
            u"л" : "l",
            u"м" : "m",
            u"н" : "n",
            u"о" : "o",
            u"п" : "p",
            u"р" : "r",
            u"с" : "s",
            u"т" : "t",
            u"у" : "u",
            u"ф" : "f",
            u"х" : "h",
            u"ц" : "c",
            u"ч" : "ch",
            u"ш" : "sh",
            u"щ" : "sht",
            u"ъ" : "y",
            u"ь" : "y",
            u"ю" : "yu",
            u"я" : "ya",
        }

        for c in title:
            if c in string.punctuation:
                title = title.replace(c, "")

        new_title = ""
        for index, c in enumerate(title):
            if c in translate_map.keys():
                new_title += translate_map[c]
            else:
                new_title += c
        new_title = new_title.replace(' ', '-')
        return new_title

    class Meta:
        managed = False
        db_table = "%s_topics" % settings.PHPBB_TABLE_PREFIX

class Post(models.Model):
    post_id   = models.BigIntegerField(primary_key=True)
    topic_id  = models.BigIntegerField()
    forum_id  = models.BigIntegerField()
    poster_id = models.BigIntegerField()
    post_time = models.BigIntegerField() # another stupid Unix timestamp

    post_username  = models.CharField(max_length=255)
    post_subject   =  models.CharField(max_length=255)
    post_text      =  models.TextField()

    def __unicode__(self):
        return "(%d) %s" % (self.pk, self.post_subject)

    def datetime(self):
        return datetime.fromtimestamp(self.post_time)



    class Meta:
        managed = False
        db_table = "%s_posts" % settings.PHPBB_TABLE_PREFIX

class User(models.Model):
    user_id   = models.BigIntegerField(primary_key=True)
    username  =  models.CharField(max_length=255)
    user_email=  models.CharField(max_length=100)

    def __unicode__(self):
        return "(%d) %s" % (self.pk, self.username)

    def gravatar_hash(self):
        return hashlib.md5(self.user_email.lower().strip()).hexdigest()

    def gravatar_url(self):
        return "//gravatar.com/avatar/%s" % self.gravatar_hash()

    class Meta:
        managed = False
        db_table = "%s_users" % settings.PHPBB_TABLE_PREFIX
