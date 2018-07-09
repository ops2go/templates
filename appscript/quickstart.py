"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Apps Script API
SCOPES = 'https://www.googleapis.com/auth/script.projects'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('script', 'v1', http=creds.authorize(Http()))

# Call the Apps Script API
try:
  # Create a new project
  request = {'title': 'My Script'}
  response = service.projects().create(body=request).execute()

  # Upload two files to the project
  request = {
    'files': [{
      'name': 'hello',
      'type': 'SERVER_JS',
      'source': 'function helloWorld() {\n  console.log("Hello, world!");\n}'
    }, {
      'name': 'appsscript',
      'type': 'JSON',
      'source': '{\"timeZone\":\"America/New_York\",\"exceptionLogging\":' + \
        '\"CLOUD\"}'
    }]
  }
  response = service.projects().updateContent(body=request,
      scriptId=response['scriptId']).execute()
  print('https://script.google.com/d/' + response['scriptId'] + '/edit')
except errors.HttpError as e:
  # The API encountered a problem.
  print(e.content)

