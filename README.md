# Show Mailing Group Members in Gmail

If you're using Google's Gmail in your company, this little plugin may come in handy.

Mailing groups are great, as long as you know who are the groups members.
In fact, you need to be able to check this quite frequently, because you never know how reliably groups are maintained, and it's the only way to make sure that your email reaches your target receipients.

This extension adds a Chrome toolbar button that detects groups in the email you're composing. It then asks a simple server to resolve those groups and lists their members in a popup.

### To get started on your machine ###
- Create a Google Service account with domain-wide authority [(Documentation)](https://developers.google.com/identity/protocols/OAuth2ServiceAccount)
- Use the following authorization scopes:
  - `https://www.googleapis.com/auth/admin.directory.group.readonly`
  - `https://www.googleapis.com/auth/admin.directory.group.member.readonly`
- Set the contstants inside `webapp/sysadmin/mailing_group.py` to your own domain configuration

### If you want to run the server on a different machine ###
- Edit the `WEBAPP_URL` inside `chrome_ext/mailing_groups/popup.js`
