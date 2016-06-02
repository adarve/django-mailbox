
import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient.discovery import build
from oauth2client import client
import os
import oauth2client
import httplib2
from oauth2client import tools
from apiclient import discovery
from googleapiclient.errors import *


"""
---------  READ BEFORE USING GMAIL API ---------

      In this page we can see a fast tutorial with how to get the client_secrets.json and
      select the gmail application.
      https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name

      Now, you have to replace the variable CLIENTSECRETS_LOCATION (after this text you can find it) value with the location of your client_secrets.json file.
      Then, replace APPLICATION_NAME (after this text you can find it) with the name of the application we are using in gmail projects

      Now, before using our modified django-mailbox, we need to execute first the function 'create_credentials()' of this file, we follow the instructions
      and we will have created the credentials.

      After it we can use django-mailbox using the API Gmail  on our django project.
"""

# Path to client_secrets.json which should contain a JSON document such as:
#   {
#     "web": {
#       "client_id": "[[YOUR_CLIENT_ID]]",
#       "client_secret": "[[YOUR_CLIENT_SECRET]]",
#       "redirect_uris": [],
#       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#       "token_uri": "https://accounts.google.com/o/oauth2/token"
#     }
#   }
CLIENTSECRETS_LOCATION = 'client_secret.json'
REDIRECT_URI = 'http://localhost'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.insert',
          'https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.insert',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
]
APPLICATION_NAME = 'Gmail API Quickstart'


class GetCredentialsException(Exception):
  """Error raised when an error occurred while retrieving credentials.

  Attributes:
    authorization_url: Authorization URL to redirect the user to in order to
                       request offline access.
  """

  def __init__(self, authorization_url):
    """Construct a GetCredentialsException."""
    self.authorization_url = authorization_url


class CodeExchangeException(GetCredentialsException):
  """Error raised when a code exchange has failed."""


class NoRefreshTokenException(GetCredentialsException):
  """Error raised when no refresh token has been found."""


class NoUserIdException(Exception):
  """Error raised when no user ID could be retrieved."""


def get_stored_credentials(user_id):
    """
    Retrieved stored credentials for the provided user ID.

    Args:
    user_id: User's ID.
    Returns:
    Stored oauth2client.client.OAuth2Credentials if found, None otherwise.
    Raises:
    NotImplemented: This function has not been implemented.
    """
    # TODO: Implement this function to work with your database.
    #       To instantiate an OAuth2Credentials instance from a Json
    #       representation, use the oauth2client.client.Credentials.new_from_json
    #       class method.
    #raise NotImplementedError()

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
        return

    credential_path = os.path.join(credential_dir,user_id)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()

    return credentials

def store_credentials(user_id, credentials):
    """Store OAuth 2.0 credentials in the application's database.

    This function stores the provided OAuth 2.0 credentials using the user ID as
    key.

    Args:
    user_id: User's ID.
    credentials: OAuth 2.0 credentials to store.
    Raises:
    NotImplemented: This function has not been implemented.
    """
    # TODO: Implement this function to work with your database.
    #       To retrieve a Json representation of the credentials instance, call the
    #       credentials.to_json() method.

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,user_id)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENTSECRETS_LOCATION, SCOPES)
        flow.user_agent = APPLICATION_NAME
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)


def exchange_code(authorization_code):
  """Exchange an authorization code for OAuth 2.0 credentials.

  Args:
    authorization_code: Authorization code to exchange for OAuth 2.0
                        credentials.
  Returns:
    oauth2client.client.OAuth2Credentials instance.
  Raises:
    CodeExchangeException: an error occurred.
  """
  flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
  flow.redirect_uri = REDIRECT_URI

  try:
    credentials = flow.step2_exchange(authorization_code)
    return credentials
  except FlowExchangeError, error:
    logging.error('An error occurred: %s', error)
    raise CodeExchangeException(None)


def get_user_info(credentials):
  """Send a request to the UserInfo API to retrieve the user's information.

  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
  user_info_service = build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None

  try:
    user_info = user_info_service.userinfo().get().execute()
  except HttpError, e:
    logging.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    return user_info
  else:
    raise NoUserIdException()

def get_authorization_url(email_address, state):
  """
  Retrieve the authorization URL.

  Args:
    email_address: User's e-mail address.
    state: State for the authorization URL.
  Returns:
    Authorization URL to redirect the user to.
  """
  flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
  flow.params['access_type'] = 'offline'
  flow.params['approval_prompt'] = 'force'
  flow.params['user_id'] = email_address
  flow.params['state'] = state
  return flow.step1_get_authorize_url(REDIRECT_URI)


def get_credentials(authorization_code, state):
  """Retrieve credentials using the provided authorization code.

  This function exchanges the authorization code for an access token and queries
  the UserInfo API to retrieve the user's e-mail address.
  If a refresh token has been retrieved along with an access token, it is stored
  in the application database using the user's e-mail address as key.
  If no refresh token has been retrieved, the function checks in the application
  database for one and returns it if found or raises a NoRefreshTokenException
  with the authorization URL to redirect the user to.

  Args:
    authorization_code: Authorization code to use to retrieve an access token.
    state: State to set to the authorization URL in case of error.
  Returns:
    oauth2client.client.OAuth2Credentials instance containing an access and
    refresh token.
  Raises:
    CodeExchangeError: Could not exchange the authorization code.
    NoRefreshTokenException: No refresh token could be retrieved from the
                             available sources.
  """
  email_address = ''
  try:
    credentials = exchange_code(authorization_code)

    user_info = get_user_info(credentials)
    email_address = user_info.get('email')
    user_id = user_info.get('id')

    if credentials.refresh_token is not None:
      store_credentials(user_id, credentials)
      return credentials
    else:
      credentials = get_stored_credentials(user_id)
      if credentials and credentials.refresh_token is not None:
        return credentials
  except CodeExchangeException, error:
    logging.error('An error occurred during code exchange.')
    # Drive apps should try to retrieve the user and credentials for the current
    # session.
    # If none is available, redirect the user to the authorization URL.
    error.authorization_url = get_authorization_url(email_address, state)
    raise error
  except NoUserIdException:
    logging.error('No user ID could be retrieved.')
  # No refresh token has been retrieved.

  authorization_url = get_authorization_url(email_address, state)
  raise NoRefreshTokenException(authorization_url)

def create_credentials():
  flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
  flow.redirect_uri = REDIRECT_URI
  authorize_url = flow.step1_get_authorize_url()
  print """
You must access to the next url, select your email account if its needed, click in 'allow', and in the next screen, go to the url of the page and copy the string after '?code=' until the hash symbol (including it into th copied string).
After it, paste the string here and push 'enter'.
"""
  print authorize_url
  print "\n"
  authorizacion_code = raw_input("Paste here the auth code: ")
  credentials = get_credentials(authorizacion_code, authorize_url)



def get_gmail_credentials(user_id):
  """
  If we don't know that user ID, we can search in the credential folder (~/credentials/), created after we called create_credentials() 
  function, the new file that has been created has our user ID as its file name.
  """
  credentials = get_stored_credentials(user_id)
  
  return credentials
