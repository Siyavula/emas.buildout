import os
import sys
import datetime
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from zope.component import getUtility
from emas.app.usercatalog import IUserCatalog
from zope.app.component.hooks import setSite
from Products.CMFCore.utils import getToolByName


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

uc = getUtility(IUserCatalog, context=portal)

for index, mid in enumerate(pmt.listMemberIds()):
    member = pmt.getMemberById(mid)
    uc.index(member)
    print "Indexing", mid
    if index % 1000 == 0:
        transaction.commit()
        print "Committing transaction"

transaction.commit()
