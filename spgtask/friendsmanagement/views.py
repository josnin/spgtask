# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from django.db.models import Q

# Create your views here.
from django.views import View
from .models import Relationship
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.core.validators import validate_email

@method_decorator(csrf_exempt, name='dispatch') #just disabled
class CreateFriendConnectionView(View):
    """1. As a user, I need an API to create a friend connection between two email addresses.

    The API should receive the following JSON request:

    {
      friends:
        [
          'andy@example.com',
          'john@example.com'
        ]
    }
    The API should return the following JSON response on success:

    {
      "success": true
    }
    Please propose JSON responses for any errors that might occur."""

    def post(self, request):
        data = json.loads(request.body)
        results = {}
        results["success"] = False
        if data.get("friends", None):
            email1, email2 = data["friends"]
            usr1 = User.objects.get(email__iexact=email1)
            usr2 = User.objects.get(email__iexact=email2)

            try:
                obj = Relationship.objects.get(user1=usr1, user2=usr2)
                return JsonResponse(results) #Do nothing    
            except Relationship.DoesNotExist:
                pass

            try:
                obj = Relationship.objects.get(user2=usr1, user1=usr2)
                return JsonResponse(results) #Do nothing    
            except Relationship.DoesNotExist:
                pass

            #not exist create new friendship
            obj = Relationship()
            obj.user1 = usr1
            obj.user2 = usr2
            obj.status = 1 # Accepted/Friends
            obj.save()

            results["success"] = True

        return JsonResponse(results)    
    

class RetrieveFriendsView(View):
    """2. As a user, I need an API to retrieve the friends list for an email address.
        The API should receive the following JSON request:
            {
              email: 'andy@example.com'
            }
        The API should return the following JSON response on success:
            {
              "success": true,
              "friends" :
                [
                  'john@example.com'
                ],
              "count" : 1   
            }	
    """

    def get(self, request):
        results = {}
        email_lst = []
        results["success"] = False
        reqst_email = request.GET.get("email", None)

        if reqst_email:

            obj = Relationship.objects.filter(Q(user1__email=reqst_email) | Q(user2__email=reqst_email), status=1) #status 1 --> Friends
            
            email_lst += list(obj.values_list("user1__email"))
            email_lst +=  list(obj.values_list("user2__email"))

            results["friends"] = list(set(email_lst))
            results["count"]  = obj.count()
            results["success"] = True

        return JsonResponse(results)


class RetrieveCommonFriendsView(View):
    """
    3. As a user, I need an API to retrieve the common friends list between two email addresses.

    The API should receive the following JSON request:

    {
      friends:
        [
          'andy@example.com',
          'john@example.com'
        ]
    }
    The API should return the following JSON response on success:

    {
      "success": true,
      "friends" :
        [
          'common@example.com'
        ],
      "count" : 1
    }
    Please propose JSON responses for any errors that might occur. """

    def get(self, request):
        #TODO: to refactor
        data = json.loads(request.body)
        results = {}
        results["success"] = False
        if data.get("friends", None):
            email1, email2 = data["friends"]

            obj1 = Relationship.objects.filter(Q(user1__email=email1) | Q(user2__email=email1), status=1) #status 1 --> Friends
            obj2 = Relationship.objects.filter(Q(user1__email=email2) | Q(user2__email=email2), status=1) #status 1 --> Friends

            obj1_email = []
            obj1_email += list(obj1.values_list("user1__email", flat=True))
            obj1_email += list(obj1.values_list("user2__email", flat=True))

            if email1 in obj1_email:
                obj1_email.remove(email1) #dont include email json request
            if email2 in obj1_email:
                obj1_email.remove(email2) #dont include email json request

            obj2_email = []
            obj2_email += list(obj2.values_list("user1__email", flat=True))
            obj2_email +=  list(obj2.values_list("user2__email", flat=True))

            if email1 in obj2_email:
                obj2_email.remove(email1) #dont include email json request
            if email2 in obj2_email:
                obj2_email.remove(email2) #dont include email json request

            count = len(set(obj1_email).intersection(obj2_email))

            results["friends"] = list(set(obj1_email).intersection(obj2_email))
            results["count"]  =  len(set(obj1_email).intersection(obj2_email))
            if count > 0:
                results["success"] = True
            else:
                results["success"] = False

        return JsonResponse(results)


@method_decorator(csrf_exempt, name='dispatch') #just disabled
class SubscribedUpdatesView(View):
    """  4. As a user, I need an API to subscribe to updates from an email address.

    Please note that "subscribing to updates" is NOT equivalent to "adding a friend connection".

    The API should receive the following JSON request:

    {
      "requestor": "lisa@example.com",
      "target": "john@example.com"
    }
    The API should return the following JSON response on success:

    {
      "success": true
    }
    Please propose JSON responses for any errors that might occur.  """

    mode = 4

    def post(self, request):
        #one way only
        data = json.loads(request.body)
        if data.get("requestor", None) and data.get("target", None):
            rqtor = data.get("requestor")
            trget = data.get("target")

            queryset1 = Relationship.objects.filter(user1__email=rqtor, user2__email=trget)

            if queryset1.exists():
                queryset1.update(status=self.mode) #subscribed
                #return {"success": True}
                return JsonResponse({"success": True})

        requestor_ins = User.objects.get(email=rqtor)
        target_ins = User.objects.get(email=trget)

        #both not exists create new subscribed/blocked
        obj = Relationship()
        obj.user1 = requestor_ins
        obj.user2 = target_ins
        obj.status = self.mode
        obj.save()
        return JsonResponse({"success": True})



class BlockedUpdatesView(SubscribedUpdatesView):
    """    5. As a user, I need an API to block updates from an email address.

    Suppose "andy@example.com" blocks "john@example.com":

    if they are connected as friends, then "andy" will no longer receive notifications from "john"
    if they are not connected as friends, then no new friends connection can be added
    The API should receive the following JSON request:

    {
      "requestor": "andy@example.com",
      "target": "john@example.com"
    }
    The API should return the following JSON response on success:

    {
      "success": true
    }
    Please propose JSON responses for any errors that might occur.
    """
    def __init__(self, *args, **kwargs):
        #override the mode subscribe --> blocked
        x = super(BlockedUpdatesView, self).__init__(*args, **kwargs)
        self.mode = 3 #blocked
        return x


@method_decorator(csrf_exempt, name='dispatch') #just disabled
class RetrieveReceiveUpdatesView(View):
    """6. As a user, I need an API to retrieve all email addresses that can receive updates from an email address.

    Eligibility for receiving updates from i.e. "john@example.com":

    has not blocked updates from "john@example.com", and
    at least one of the following:
    has a friend connection with "john@example.com"
    has subscribed to updates from "john@example.com"
    has been @mentioned in the update
    The API should receive the following JSON request:

    {
      "sender":  "john@example.com",
      "text": "Hello World! kate@example.com"
    }
    The API should return the following JSON response on success:

    {
      "success": true
      "recipients":
        [
          "lisa@example.com",
          "kate@example.com"
        ]
    }
    Please propose JSON responses for any errors that might occur."""

    def post(self, request):
        data = json.loads(request.body)
        results = {}
        results["success"] = False
        if data.get("sender", None) and data.get("text", None):
            sender = data.get("sender")
            text = data.get("text")
            rlt_qset = Relationship.objects.all()
            emails1 = rlt_qset.filter(user2__email=sender, status=4).values_list("user1__email", flat=True) # has subsrbied
            emails2 = rlt_qset.filter(user1__email=sender, status=1).values_list("user2__email", flat=True) # has a friend connection
            emails3 = rlt_qset.filter(user2__email=sender, status=1).values_list("user1__email", flat=True) # has a friend connection

            recipients = list(emails1) + list(emails2) + list(emails3)

            for e in text.split(" "):
                if "@" in e:
                    try:
                        validate_email(e)
                        recipients.append(e)
                    except:
                        #not valid email
                        pass

            results["recipients"] = recipients
            results["success"] = True

        return JsonResponse(results)

