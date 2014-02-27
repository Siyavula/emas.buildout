import os
import sys
import datetime
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from ZODB.POSException import ConflictError

from zope.component import getUtility
from zope.intid import queryId
from zope.intid import IIntIds
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
ints = getUtility(IIntIds)  

for index, mid in enumerate(pmt.listMemberIds()):
    member = pmt.getMemberById(mid)
    if ints.queryId(member) is not None:
        uc.index(member)
        print "Indexing", mid
    else:
        print "Already indexed", mid
    if index % 1000 == 0:
        try:
            print "Committing transaction"
            transaction.commit()
        except ConflictError as e:
            print 'Could not commit after' % index

transaction.commit()
