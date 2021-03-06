from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly',
          'https://www.googleapis.com/auth/admin.directory.group.readonly']


def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # list_users(service)
    list_groups(service)


def list_groups(service):
    print('GroupName;GroupEmail;MemberEmail;MemberStatus')

    unique_members = {}
    groups_of_members = {}

    results = service.groups().list(domain='giesserei-gesewo.ch').execute()
    groups = results.get('groups', [])

    for group in groups:
        # query member list
        group_id = group.get('id')
        group_name = group.get('name', '')
        group_email = group.get('email', '')

        member_results = service.members().list(groupKey=group_id).execute()
        members = member_results.get('members', [])

        for member in members:
            member_id = member['id']
            member_email = member.get('email', '')

            unique_members[member_email] = member

            if member_id not in groups_of_members:
                groups_of_members[member_id] = set()

            groups_of_members[member_id].add(group_name)

            print(u'{0};{1};{2};{3};{4}'.format(
                group_name,
                group_email,
                member_id, member_email, member.get('status', '-')))

    print("MemberEmail:GroupNames")
    for k, member in sorted(unique_members.items()):
        member_email = member.get('email', '')
        member_id = member.get('id', '')
        groups = sorted(groups_of_members[member_id])
        groups_s = ", ".join(e for e in groups)
        print(u'"{0}"; "{1}"'.format(member_email, groups_s))


def list_users(service):
    # Call the Admin SDK Directory API
    print('Getting the first 10 users in the domain')
    results = service.users().list(customer='my_customer', maxResults=10,
                                   orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print(u'{0} ({1})'.format(user['primaryEmail'],
                                      user['name']['fullName']))


if __name__ == '__main__':
    main()
