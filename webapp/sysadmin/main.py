from operator import itemgetter
from flask import Flask
from flask.templating import render_template
from sysadmin.mailing_groups import AdminService

app = Flask(__name__)

admin_svc = AdminService()


@app.route("/")
def hello():
    return '<html><body><a href="mailinggroups">Mailing Groups</a></body></html>'


@app.route('/mailinggroups')
def mailing_groups():
    groups = sorted(admin_svc.groups(), key=itemgetter('name'))
    return render_template('groups.html', groups=groups)


@app.route('/mailinggroups/<item_id>/members')
def group_members(item_id):
    grp_id, level = item_id.split('_')
    members = sorted(admin_svc.members(grp_id), key=itemgetter('name'))
    return render_template('members.html', members=members, level=int(level) + 1)


@app.route('/mailinggroups/resolve/<email_list>')
def resolve_gmail_field(email_list):
    groups = sorted(admin_svc.resolve(email_list), key=itemgetter('name'))
    return render_template('groups.html', groups=groups)
