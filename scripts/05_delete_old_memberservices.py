import os
import sys
import datetime
import shutil

import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility


app = makerequest.makerequest(app)
portal = getattr(app, sys.argv[-1])

user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))
portal.setupCurrentSkin(portal.REQUEST)

start = datetime.datetime.now()
print 'Starting at:%s' % start.strftime('%H:%M:%S:%s')
if 'memberservices' in portal.objectIds():
    portal._delObject('memberservices', suppress_events=True)

query = {'portal_type': 'emas.app.memberservice'}
catalog = portal.portal_catalog
brains = catalog(query)
for counter, brain in enumerate(brains):
    number = str(counter+1)
    print 'Processing item %s of %s' % (number, len(brains))
    catalog.uncatalog_object(brain.getPath())
    if not counter % 10000:
        print 'Commiting transaction.'
        transaction.commit()

brains = catalog(query)
print len(brains)
print 'Commiting transaction.'
transaction.commit()
end = datetime.datetime.now()
print 'Done at:%s' % end.strftime('%H:%M:%S:%s')
print 'Elapsed time=%s seconds' % (end-start).seconds
print '----------------------------------------------'
