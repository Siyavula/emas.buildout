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
    query = {'portal_type':'emas.app.order',
             'path': '/'.join(orders.getPhysicalPath())}
    brains = portal_catalog(query)
    print('A total of %s orders will be migrated.' % len(brains))
    m_start = datetime.datetime.now()
    print('Migration started at %s' % m_start.strftime(TIME_FORMAT))
    for count, brain in enumerate(brains):
        start = datetime.datetime.now()
        print('Start order:%s at %s' % (count+1, start.strftime(TIME_FORMAT)))

        order = brain.getObject() 
        portal_catalog.uncatalog_object('/'.join(order.getPhysicalPath()))
        for item in order.order_items():
            print('Uncataloging order item:%s' % item.getId())
            portal_catalog.uncatalog_object('/'.join(item.getPhysicalPath()))
        print('Indexing in custom catalog.')
        order.reindexObject()
        finish = datetime.datetime.now()
        print('Finished order:%s at %s' % (count, finish.strftime(TIME_FORMAT)))
        print('It took %s seconds.' % (finish - start).seconds)
        if not (count % 1000):
            print('Commiting 1000 orders.')
            transaction.commit()

    m_end = datetime.datetime.now()
    print('Completed at:%s' % m_end.strftime(TIME_FORMAT))
    print('Migration took %s seconds.' % (m_end - m_start).seconds)
    print('A total of %s orders were migrated.' % len(brains))
    print '-------------------------------------------------------------------'


# Setup the environment for the script and make sure we have all required values
# app is bound for us, when this script starts.

try:
    portal_id = sys.argv[1]
except IndexError:
    portal_id = 'Plone' 

if not app.hasObject(portal_id):
    print 'Please specify the id of your plone site as the first argument '
    print 'to this script.'
    print 'Usage: <instancehome>/bin/instance run %s <id>' % sys.argv[0]
    sys.exit(1)

portal = app[portal_id]
setSite(portal)

# we assume there is an admin user
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))

process(portal)

transaction.commit()
