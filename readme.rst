Django-Mailbox - API Gmail extension
====================================

This Django-Mailbox extension is focused on using the API of gmail for getting new emails we receive in our mailbox.

The modification is located on "django_mailbox/models.py", and a new file is added in the same directory, "server_side_gmail.py" which contains the functions to provide the retrieve, creation and store of the right credentials to connect with the Gmail API.


Tutorial - *Read before using this package*
===========================================

- In this `page <https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name>`_ we can see a fast tutorial with how to get the client_secrets.json and select the gmail application.


- Now, you have to replace the variable CLIENTSECRETS_LOCATION (after this text you can find it) value with the location of your client_secrets.json file.
- Then, replace APPLICATION_NAME (after this text you can find it) with the name of the application we are using in gmail projects.

- Now, before using our modified django-mailbox, we need to execute first the function 'create_credentials()' of this file, we follow the instructions and we will have created the credentials.

- After it we can use django-mailbox using the API Gmail  on our django project.

- You can install it with 'python setup.py install'.

Django Mailbox Documentation
============================
- Documentation for django-mailbox is available on
  `ReadTheDocs <http://django-mailbox.readthedocs.org/>`_.

