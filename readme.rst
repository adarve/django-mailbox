Django-Mailbox - Gmail API extension
====================================

This Django-Mailbox extension is focused on using the API of gmail for getting new emails we receive in our mailbox.

Django Mailbox Documentation
============================
- Documentation for django-mailbox is available on
  `ReadTheDocs <http://django-mailbox.readthedocs.org/>`_.

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/coddingtonbear/django-mailbox
   :target: https://gitter.im/coddingtonbear/django-mailbox?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Guide - Gmail API extension
===========================

- Firstly, we follow the guide of this `page <https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name>`_ . What we need essentialy is our "client_secrets.json", select the gmail application, and install the Google Client Library, with the following command:
   $ pip install --upgrade google-api-python-client

- The next step is to download or clone this modified django-mailbox package repository.

- Open the "/django_mailbox/transports/server_side_gmail.py" file, and replace the variable '**CLIENTSECRETS_LOCATION**' value with the location of your "client_secrets.json" file. (If the file is in the same directory as 'server_side_gmail.py' the location will be just the name of the file, if its in another path it's recommended to set the value as the full path of the json file)

- Then, replace '**APPLICATION_NAME**' value (on "/django_mailbox/transports/server_side_gmail.py" file ) with the name of the application you are using in gmail projects (the one we selected in the first step).

- Execute the python file 'create_credentials.py', located in the same directory as "django_mailbox/transports/server_side_gmail.py".
      $ python create_crendentials.py
   Now we follow the instructions and then, the credentials will be created.

   If you are accessing the server remotely, execute the following command.
      $ python create_credentials.py --noauth_local_webserver        

- After the last command finishes, it will show our user_id. A file with the same name as our user_id is created in the credential folder (~/credentials/). If we forget to copy the id we can find it in that folder, in the name itself of the new credentials file.

- Now,  we can install django-mailbox with Gmail API extension to use it on our django project, using the right URI. Go to the root folder of this package, and install it with the next command: 
      $ python setup.py install.

- The URI to use the gmail api transport, contains the user email, the user id and the watch address in case we are using the pub sub feature of google cloud platform.
  An example of an URI with gmail api:
     'gmailapi+ssl://<username>%40<yourdomain.com>:<user_id>@/adress/to/watch/pubsub'

- Allow account access for less secure apps on Gmail:
  https://support.google.com/accounts/answer/6010255?hl=en


