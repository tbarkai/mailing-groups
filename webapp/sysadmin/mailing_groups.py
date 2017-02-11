from itertools import product, chain
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from httplib2 import Http

DOMAIN = 'example.com'
ADMIN_ACCOUNT = 'admin@example.com'
KEYFILE = 'secret/account-credentials.json'

scopes = [
    'https://www.googleapis.com/auth/admin.directory.group.readonly',
    'https://www.googleapis.com/auth/admin.directory.group.member.readonly'
]


class AdminService:

    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scopes=scopes)
        delegated_credentials = credentials.create_delegated(ADMIN_ACCOUNT)
        http_auth = delegated_credentials.authorize(Http())
        self.service = build('admin', 'directory_v1', http=http_auth)

    def groups(self):
        gapi_response = self.service.groups().list(domain=DOMAIN).execute()
        return gapi_response['groups']

    def members(self, grp_id):
        gapi_response = self.service.members().list(groupKey=grp_id).execute()
        if 'members' not in gapi_response:
            return ['--- Empty ---']

        members = gapi_response['members']

        # incredibly, there can be a user without an email defined
        with_email = [m for m in members if 'email' in m]
        for m in with_email:
            self._add_name(m)

        return with_email

    def resolve(self, emails):
        gapi_response = self.service.groups().list(domain=DOMAIN).execute()
        groups = gapi_response['groups']
        aliases_lists = (product([g['email']] + g['nonEditableAliases'], [g]) for g in groups)
        aliases_flat = chain.from_iterable(aliases_lists)
        d = dict(aliases_flat)
        requested_groups = (d[x] for x in emails.split(',') if x in d)
        return requested_groups

    @staticmethod
    def _add_name(member):
        email = member["email"]
        if email.endswith(DOMAIN):
            s = email.split('@')[0]
            if member['type'] == 'USER':
                s = s.replace('.', ' ').title()
        else:
            s = email
        member['name'] = s
