# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Relationship(models.Model):

    RELATIONSHIP_CHOICES = (
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'Decline'),
        (3, 'Blocked'),
        (4, 'Subscribed'),
    )
        

    user1 = models.ForeignKey(User, related_name="relationship_user1")
    user2 = models.ForeignKey(User, related_name="relationship_user2")
    status = models.IntegerField(choices=RELATIONSHIP_CHOICES, default=0)
