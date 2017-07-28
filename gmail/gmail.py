import argparse
import base64
from email.mime.text import MIMEText

from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials
from ratelimiter import RateLimiter

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--sender', required=True)
  parser.add_argument('--receiver', required=True)
  args = parser.parse_args()

  test_subject = 'Test'
  msg_txt = 'Hello world'
  msg = create_message(args.sender, args.receiver, test_subject, msg_txt)
  send_message(get_gmail(), message=msg)

def get_gmail():
  credentials = GoogleCredentials.get_application_default()
  gmail_api = discovery.build('gmail', 'v1', credentials=credentials)
  return gmail_api

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id='me', message=None):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

if __name__ == '__main__':
    main()
