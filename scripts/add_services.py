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

portal = app.emas
setSite(portal)
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))
setSite(portal)
portal.changeSkin('Plone Default')
wf = getToolByName(portal, 'portal_workflow')

products_and_services = portal['products_and_services']

def add_service(id, **kw):
    if not products_and_services.hasObject(id):
        print "Adding service " + id
        products_and_services.invokeFactory(id=id, type_name='emas.app.service',
            service_type='subscription', amount_of_credits=0, **kw)
        ob = products_and_services[id]
        wf.doActionFor(ob, 'publish')
        # Reindex, probably to get the Title right if memory serves
        ob.reindexObject()
        return ob
    return None

# Create services
add_service('maths-grade8-practice',
    price=80.0, grade=u'grade-8', subscription_period=365,
    access_path='@@practice/grade-8', subject=u'maths',
    title=u'Maths Grade 8 Intelligent Practice')
add_service('maths-grade9-practice',
    price=80.0, grade=u'grade-9', subscription_period=365,
    access_path='@@practice/grade-9', subject=u'maths',
    title=u'Maths Grade 9 Intelligent Practice')

# Create monthly services
add_service('maths-grade8-monthly-practice',
    price=15.0, grade=u'grade-8', subscription_period=30,
    access_path='@@practice/grade-8', subject=u'maths',
    title=u'Maths Grade 8 Intelligent Practice')
add_service('maths-grade9-monthly-practice',
    price=15.0, grade=u'grade-9', subscription_period=30,
    access_path='@@practice/grade-9', subject=u'maths',
    title=u'Maths Grade 9 Intelligent Practice')

transaction.commit()
