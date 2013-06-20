import os
import sys
import datetime
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from zope.app.component.hooks import setSite
from Products.CMFCore.utils import getToolByName

from emas.app.browser import utils


def process(portal, pmt):
    import pdb;pdb.set_trace()
    mids = pmt.listMemberIds()
    total = len(mids)
    print '--------------------------------START-------------------------------'
    print 'Processing a total of %s members.' % total
    uids = utils.practice_service_uuids(portal)
    for count, mid in enumerate(mids):
        for subject in ['maths', 'science']:
            memberservices = utils.member_services_for_subject(portal, uids, mid)
            print 'Processing member:%s - number %s of %s.' % (mid, count+1, total)
            if not memberservices:
                #print 'Skipping... no active member services.'
                continue
            print 'Unifying member services.'
            ms[0].merge_memberservices(memberservices)
    print '--------------------------------DONE-------------------------------'


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

# Now do the work
process(portal, pmt)

# Better commit the work too
#transaction.commit()
