import os
import sys
from datetime import datetime, timedelta, date
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from zope.app.component.hooks import setSite
from Products.CMFCore.utils import getToolByName

def commit(count):
    print '************************************************************'
    print 'Committing transaction. Count = ', count
    try:
        transaction.commit()
    except ConflictError: 
        print "Could not commit transaction, restarting transaction."
        # start a new transaction
        transaction.begin() 

def process(portal, pmt):
    
    # iterate over all members and add the registration date, set it to be
    # (arbitrarily) a month ago from current date.
    count = 0
    for member in pmt.listMembers():
        #oldest member service creation date
        month_ago = datetime.now() - timedelta(1*365/12) # subtract a month
        registration_date = member.getProperty('registrationdate')
        if registration_date == None:
            member.setMemberProperties(mapping={"registrationdate": month_ago})
            count += 1

        if count % 100 == 0:
            commit(count)

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
transaction.commit()
