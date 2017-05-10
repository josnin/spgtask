# spgtask


Background

For any application with a need to build its own social network, "Friends Management" is a common requirement which usually starts off simple but can grow in complexity depending on the application's use case.

Usually, applications would start with features like "Friend", "Unfriend", "Block", "Receive Updates" etc.

Your Task

Develop an API server that does simple "Friend Management" based on the User Stories below.

You are required to:

Deploy an instance of the API server on the public cloud or provide a 1-step command to run your API server locally, e.g. using a Makefile or Docker Compose) for us to test run the APIs
Write sufficient documentation for the APIs and explain your technical choices
User Stories

1. As a user, I need an API to create a friend connection between two email addresses.

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
Please propose JSON responses for any errors that might occur.

2. As a user, I need an API to retrieve the friends list for an email address.

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
Please propose JSON responses for any errors that might occur.

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
Please propose JSON responses for any errors that might occur.

4. As a user, I need an API to subscribe to updates from an email address.

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
Please propose JSON responses for any errors that might occur.

5. As a user, I need an API to block updates from an email address.

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

6. As a user, I need an API to retrieve all email addresses that can receive updates from an email address.

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
Please propose JSON responses for any errors that might occur.



How to Use the API?

1) Manually create all the users/email need to work on the FriendsManagement API

![image](https://cloud.githubusercontent.com/assets/3206118/25900608/9573d5f0-35c6-11e7-8206-ad19cfb6cbb0.png)

2) List of API

  1 - http://localhost:8000/api/create_friend
  2 - http://localhost:8000/api/retrieve/
  3 - http://localhost:8000/api/retrieve_common_friends/
  4 - http://localhost:8000/api/subscribed_updates/
  5 - http://localhost:8000/api/blocked_updates/
  6 - http://localhost:8000/api/retrieve_receive_updates/
