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

from logging import getLogger

TIME_FORMAT = '%H:%M:%S:%s'

def process(portal):
    print '-------------------------------------------------------------------'
    print('Started at:%s' % datetime.datetime.now().strftime(TIME_FORMAT))
    portal_catalog = getToolByName(portal, 'portal_catalog')
    order_catalog = getToolByName(portal, 'order_catalog')

    orders = portal.orders
    order_ids = orders.objectIds()
    print("A total of %s orders will be migrated.:" % len(orders))
    for count, order_id in enumerate(order_ids):
        start = datetime.datetime.now()
        print('Start order:%s at %s' % (count, start.strftime(TIME_FORMAT)))
        order = orders[order_id]
        portal_catalog.uncatalog_object('/'.join(order.getPhysicalPath()))
        for item in order.order_items():
            portal_catalog.uncatalog_object('/'.join(item.getPhysicalPath()))
        order_catalog.reindexObject(order)
        finish = datetime.datetime.now()
        print('Finished order:%s at %s' % (count, finish.strftime(TIME_FORMAT)))
        print('It took %s seconds.' % (finish - start).seconds)

    print('Completed at:%s' % datetime.datetime.now().strftime(TIME_FORMAT))
    print '-------------------------------------------------------------------'


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

process(portal)

# transaction.commit()
