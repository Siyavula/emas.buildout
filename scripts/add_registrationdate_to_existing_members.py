import os
import sys
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from zope.app.component.hooks import setSite
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

# Setup the environment for the script and make sure we have all required values
# app is bound for us, when this script starts.

try:
    portal_id = sys.argv[1]
except IndexError:
    portal_id = 'Plone' 

if not app.hasObject(portal_id):
    print "Please specify the id of your plone site as the first argument "
    print "to this script."
    print "Usage: <instancehome>/bin/instance run %s <id>" % sys.argv[0]
    sys.exit(1)

portal = app[portal_id]
setSite(portal)

# we assume there is an admin user
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))
pmt = getToolByName(portal, 'portal_membership')

# iterate over all members and set the registration date to the
# oldes creation date of the member services for the given user.

count = 0
pc = getToolByName(portal, 'portal_catalog')

for member in pmt.listMembers():
    registration_date = member.getProperty('registrationdate')

    if not registration_date == DateTime("1970/01/01 00:00:00 GMT+2"):
        continue

    query = {'portal_type': 'emas.app.memberservice',
             'userid': member.getId() }
    cdates = [b.created for b in pc(query)]
    if cdates:
        cdates.sort()
        regdate = cdates[0]
    else:
        continue

    print "Setting registration date for %s to %s" % (
        member.getId(), regdate
        )
    member.setMemberProperties(mapping={"registrationdate": regdate})
    count += 1

    if count % 100 == 0:
        print 'Committing transaction. Count = ', count
        try:
            transaction.commit()
        except ConflictError: 
            print "Could not commit transaction, restarting transaction."
            # start a new transaction
            transaction.begin() 


transaction.commit()
