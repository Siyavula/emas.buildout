import os
import sys
import datetime
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from ZODB.POSException import ConflictError

from zope.component import getUtility
from zope.intid import IIntIds
from zope.index.field import FieldIndex
from emas.app.usercatalog import IUserCatalog
from zope.app.component.hooks import setSite
from Products.CMFCore.utils import getToolByName

from BTrees.IOBTree import IOBTree

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
# we added _regdate later so we can't assume the catalog has this index
# yet
if not hasattr(uc, '_regdate'):
    uc._regdate = FieldIndex()
if not hasattr(uc, '_metadata'):
    uc._metadata = IOBTree()
ints = getUtility(IIntIds)  

for index, mid in enumerate(pmt.listMemberIds()):
    member = pmt.getMemberById(mid)
    mintid = ints.queryId(member)

    regdate = member.getProperty('registrationdate')
    regdate = datetime.datetime.strptime(
        regdate.strftime("%Y-%m-%d"), "%Y-%m-%d")

    if not uc._metadata.has_key(mintid):
        uc.index(member)
        print "Indexing", mid
    elif uc._metadata.has_key(mintid):
        md = uc._metadata[mintid]
        if md['registrationdate'] != regdate:
            print "Re-indexing", mid
        else:
            print "Already indexed", mid

    if index % 1000 == 0:
        try:
            print "Committing transaction"
            transaction.commit()
        except ConflictError as e:
            print 'Could not commit after', index
            # start a new transaction
            transaction.begin() 

transaction.commit()
