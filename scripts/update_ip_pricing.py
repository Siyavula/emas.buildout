import os
import sys
import datetime
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from plone.uuid.interfaces import IUUID
from zope.app.component.hooks import setSite
from Products.CMFCore.utils import getToolByName

from emas.app.browser import utils

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

service_ids = [
    'maths-grade8-practice',
    'maths-grade9-practice',
    'maths-grade10-practice',
    'maths-grade11-practice',
    'maths-grade12-practice',
    'science-grade10-practice',
    'science-grade11-practice',
    'science-grade12-practice',
]

products_and_services = portal['products_and_services']

for sid in service_ids:
    service = products_and_services[sid]
    service.subscription_period = 365
    # the total price for the 3 grades should amount to R400, this is why
    # we have such odd prices
    if sid.startswith('maths'):
        service.price = 80 # 5 services, R400
    elif sid in ('science-grade12-practice',):
        service.price = 134 # 3 services, total must be R400
    else:
        service.price = 133
    print "Updating pricing and subscription period for ", service.Title()

transaction.commit()
