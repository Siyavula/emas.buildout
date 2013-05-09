import sys
import datetime
import transaction
from types import ListType

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from zope.app.component.hooks import setSite
from ZODB.POSException import ConflictError


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
app = makerequest.makerequest(app)
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))

today = datetime.datetime.today()

for ms_id in portal.memberservices.objectIds():

    ms = portal.memberservices._getOb(ms_id)

    if ms.expiry_date < today:
        print "%s expiring on %s" % (ms.absolute_url(), ms.expiry_date)
        print "Deleting ", ms.absolute_url()
        portal.memberservices.manage_delObjects(ids=ms_id)

    if count % 1000 == 0:
        print '************************************************************'
        print 'Committing transaction.'
        try:
            transaction.commit()
        except ConflictError: 
            # start a new transaction
            transaction.begin() 

transaction.commit()
