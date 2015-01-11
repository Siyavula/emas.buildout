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

# Create services
products_and_services.invokeFactory(type_name='emas.app.service',
    id='maths-grade8-practice', price=80.0, grade=u'grade-8',
    service_type='subscription', subscription_period=365,
    amount_of_credits=0, access_path='@@practice/grade-8',
    subject=u'maths', title=u'Maths Grade 8 Intelligent Practice')
products_and_services.invokeFactory(type_name='emas.app.service',
    id='maths-grade9-practice', price=80.0, grade=u'grade-9',
    service_type='subscription', subscription_period=365,
    amount_of_credits=0, access_path='@@practice/grade-9',
    subject=u'maths', title=u'Maths Grade 9 Intelligent Practice')

# Publish
wf.doActionFor(products_and_services['maths-grade8-practice'], 'publish')
wf.doActionFor(products_and_services['maths-grade9-practice'], 'publish')

# Reindex, probably to get the Title right if memory serves
products_and_services['maths-grade8-practice'].reindexObject()
products_and_services['maths-grade9-practice'].reindexObject()

transaction.commit()
