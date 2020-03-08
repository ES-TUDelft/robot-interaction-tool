import os
from google.oauth2 import service_account

DIALOGFLOW_PROJECT_ID = 'ivy-gciewv'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_CREDENTIALS_FILE = "{}/robot_manager/pepper/hre_chat/credentials_smalltalk.json".format(os.getcwd())
GOOGLE_CREDENTIALS_FROM_SERVICE_ACCOUNT = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE)

with open(GOOGLE_CREDENTIALS_FILE, 'r') as file:
    GOOGLE_CLOUD_CREDENTIALS = file.read()