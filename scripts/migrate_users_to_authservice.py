# Boilerplate.
import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from zope.app.component.hooks import setSite

app = makerequest.makerequest(app)
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))
portal = app.emas
setSite(portal)
portal.changeSkin('Plone Default')
# End Boilerplate.

import json
import urllib2
from Products.CMFCore.utils import getToolByName
from emas.app.memberservice import MemberServicesDataAccess

class Request(urllib2.Request):
    def __init__(self, url, method=None):
        urllib2.Request.__init__(self, url)
        self.method = method

    def get_method(self):
        if self.method is None:
            return urllib2.Request.get_method(self)
        else:
            return self.method

def create_user(last_login, pwh, **kw):
    data = {
        "identifiers": {
        },
        "password_method": "plone",
        "password_salt": "",
        "password_hash": pwh,
        "last_login": last_login
    }
    data['identifiers'].update(kw)
    req = Request('http://localhost:6544/users', 'POST')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    if response.code == 200:
        result = json.loads(response.read())
        return result['user']['user_id']
    return None

def update_profile(uuid, **kw):
    data = {}
    data.update(kw)

    req = Request('http://localhost:6543/update/{}'.format(uuid), 'PUT')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    return response.code == 200

uf = getToolByName(portal, 'acl_users')
pwmap = uf.source_users._user_passwords
msdao = MemberServicesDataAccess(portal)

# Traverse the password map in source_users, as this is much less expensive
# than using acl_users.getUsers or portal_membership.listMembers. Fetch each
# member separately.
total = len(pwmap)
count = 0
for uid, pw in pwmap.items():
    member = uf.getUser(uid)
    pw = pwmap.get(uid, None)

    # A quick inspection on live indicates all users have SSHA passwords.
    if pw is not None and pw.startswith('{SSHA}'):
        password = pw[6:]

        # Other details we need
        fullname = member.getProperty('fullname')
        email = member.getProperty('email')
        role = member.getProperty('userrole')
        school = member.getProperty('school')
        province = member.getProperty('province')
        newsletter = member.getProperty('subscribe_to_newsletter')
        registered = member.getProperty('registrationdate')
        last_login = member.getProperty('last_login_time').ISO()

        # Split fullname into name and surname
        if fullname != '':
            entries = fullname.strip().split()
            name = ' '.join(entries[:-1])
            surname = entries[-1] if len(entries) > 1 else None
        else:
            name = surname = None

        # member services
        memberservices = [s.related_service(portal).id for s in \
            msdao.get_active_memberservices(uid)]

        # First create the user in the auth service, that will give you his
        # uuid, use that to register the profile details.
        uuid = create_user(last_login, password, username=uid, email=email)
        if uuid is not None:
            update_profile(uuid,
                general = {
                    'name': name,
                    'surname': surname,
                    'username': uid,
                    'email': email,
                },
                emas = {
                    'registrationdate': registered.ISO(),
                    'memberservices': memberservices
                }
            )

        count += 1
        if count % 50 == 0:
            print "Migrated {0} of {1}".format(count, total)
print "Migrated {0} users".format(count)
