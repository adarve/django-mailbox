Django-Mailbox - Gmail API extension
====================================

This Django-Mailbox extension is focused on using the API of gmail for getting new emails we receive in our mailbox.

The modification is located on "django_mailbox/models.py", and a new file is added in the same directory, "server_side_gmail.py" which contains the functions to provide the retrieve, creation and store of the right credentials to connect with the Gmail API.


Tutorial - *Read before using this package*
===========================================

- In this `page <https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name>`_ we can see a fast tutorial with how to get the client_secrets.json and select the gmail application.

- Now, you have to replace the variable CLIENTSECRETS_LOCATION (on "/django_mailbox/server_side_gmail.py" file) value with the location of your client_secrets.json file.
- Then, replace APPLICATION_NAME (on "/django_mailbox/server_side_gmail.py" file ) with the name of the application we are using in gmail projects.

- Now, before using our modified django-mailbox, we need to execute first the function 'create_credentials()' of "django_mailbox/server_side_gmail.py" file, we follow the instructions and then, the credentials will be created.

- Then, inside the function "get_new_mail(self, condition=None)" from "models.py", there is a call to
      "server_side_gmail.get_gmail_credentials(user_id)" in which we have to insert our user_id as the parameter. 
      
          Note: If we don't know that user ID, we can search in the credential folder (~/credentials/), created after we called "create_credentials()" function, the new file that has been created has our user ID as its filename.

- Now, all its prepared, and we can use django-mailbox using the Gmail API on our django project.
  The package can be installed with 'python setup.py install' command.

Django Mailbox Documentation
============================
- Documentation for django-mailbox is available on
  `ReadTheDocs <http://django-mailbox.readthedocs.org/>`_.

