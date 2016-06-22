
Easily ingest messages from POP3, IMAP, Gmail API or local mailboxes into your Django application.

This app allows you to either ingest e-mail content from common e-mail services (as long as the service provides POP3 or IMAP support),
or directly recieve e-mail messages from ``stdin`` (for locally processing messages from Postfix or Exim4).

These ingested messages will be stored in the database in Django models and you can process their content at will,
or -- if you're in a hurry -- by using a signal receiver.

- Documentation for django-mailbox is available on
  `ReadTheDocs <http://django-mailbox.readthedocs.org/>`_.
- Please post issues on
  `Github <http://github.com/coddingtonbear/django-mailbox/issues>`_.
- Test status available on
  `Travis-CI <https://travis-ci.org/coddingtonbear/django-mailbox>`_.


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

- After the last command finishes, it will show our user_id. A file with the same name as our user_id is created in the credential folder (~/credentials/). If we forget to copy the id we can find it in that folder.

- Now, all its prepared, and we can use install django-mailbox with Gmail API extension to use it on our django project, using the right URI.

-  Go to the root folder of this package, and install it with the next command: python setup.py install.
