import os
import sys
import datetime
import transaction
from time import sleep

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

today = datetime.date.today()

count = 0
expired = 0
committed = False

memberlog = open(
    os.path.join(os.environ['CLIENT_HOME'], 'deletemembers.dat'), 'a'
    )

runtime_start = 0
runtime_end = 4

def commit():
    print '************************************************************'
    print 'Committing transaction. Count = ', count
    try:
        transaction.commit()
        committed = True
    except ConflictError: 
        print "Could not commit transaction, restarting transaction."
        # start a new transaction
        transaction.begin() 

for ms_id in portal.memberservices.objectIds():

    count += 1

    ms = portal.memberservices._getOb(ms_id)
    now = datetime.datetime.now()

    while not (runtime_start <= now.hour < runtime_end):
        if not committed:
            commit()
        print "sleeping"
        sleep(60)
        now = datetime.datetime.now()

    if ms.expiry_date < today:
        print "%s expiring on %s" % (ms.absolute_url(), ms.expiry_date)
        print "Deleting ", ms.absolute_url()
        memberlog.write(
            "%s,%s,%s,%s,%s\n" % (ms.userid, 
                                  ms.related_service.to_id,
                                  ms.expiry_date,
                                  ms.credits,
                                  ms.service_type)
            )
        portal.memberservices.manage_delObjects(ids=ms_id)
        expired += 1
        committed = False

    if count % 100 == 0:
        commit()

print "Expired: ", expired
print "Total active member services: ", len(portal.memberservices.objectIds())
memberlog.close()
transaction.commit()
