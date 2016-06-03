Django-Mailbox - Gmail API extension
====================================

This Django-Mailbox extension is focused on using the API of gmail for getting new emails we receive in our mailbox.

The modification is located on "django_mailbox/models.py", and a new file is added in the same directory, "server_side_gmail.py" which contains the functions to provide the retrieve, creation and store of the right credentials to connect with the Gmail API.


Tutorial - Getting Gmail API credentials --- *Read before using this package*
===========================================

- First, download our "client_secrets.json" an select the gmail application. In this `page <https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name>`_ there is a fast guide about how to do it.

- The next step is to download or clone this modified django-mailbox package repository. 

- Open the "/django_mailbox/server_side_gmail.py" file, and replace the variable '**CLIENTSECRETS_LOCATION**' value with the location of your "client_secrets.json" file. (If the file is in the same directory as 'server_side_gmail.py' the location will be just the name of the file, if its in another path it's recommended to set the value as the full path of the json file)

- Then, replace '**APPLICATION_NAME**' value (on "/django_mailbox/server_side_gmail.py" file ) with the name of the application you are using in gmail projects (the one we selected in the first step).

- Execute the python file 'create_credentials.py', located in the same directory as "django_mailbox/server_side_gmail.py".
      Command: **python create_crendentials.py**
      Now we follow the instructions and then, the credentials will be created.

- Open the file "/django_mailbox/models.py", in the function "**get_new_mail(self, condition=None)", there is a call to  "server_side_gmail.get_gmail_credentials(user_id)**" in which we have to insert **our user_id** as the parameter. 
      
      Note: If we don't know that user ID, we can search in the credential folder (~/credentials/), created after we called "create_credentials()" function, the new file that has been created has our user ID as its filename.

- Now, all its prepared, and we can use install django-mailbox with Gmail API extension to use it on our django project.
  Go to the root folder of this package, and install it with the next command: **python setup.py install**.

Django Mailbox Documentation
============================
- Documentation for django-mailbox is available on
  `ReadTheDocs <http://django-mailbox.readthedocs.org/>`_.

