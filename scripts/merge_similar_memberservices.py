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


def is_similar_to(self, other):
    attrs = ['grade', 'subject', 'access_path']
    for attr in attrs:
        self_attr = getattr(self.related_service.to_object, attr, None)
        other_attr = getattr(other.related_service.to_object, attr, None)
        if self_attr != other_attr:
            return False
    return True


def merge_with(self, other):
    if other.expiry_date > self.expiry_date:
        print '    Changing expiry date from %s to %s' % (self.expiry_date,
                                                          other.expiry_date)
        self.expiry_date = other.expiry_date
    self_subs_period = self.related_service.to_object.subscription_period
    other_subs_period = other.related_service.to_object.subscription_period
    if other_subs_period > self_subs_period:
        self.related_service = other.related_service


def merge_memberservices(portal, memberservices):
    service1, service2 = memberservices
    if is_similar_to(service1, service2):
        print '    %s and %s are similar, merging...' % (
            service1.Title(), service2.Title()
        )
        merge_with(service1, service2)
        print '    Deleting %s' % service2.getId()
        portal.memberservices.manage_delObjects([service2.getId()])


def process(portal, pmt):
    suids = []
    for subject in ('maths', 'science'):
        for grade in (10, 11, 12):
            sid = '%s-grade%s-monthly-practice' % (subject, grade)
            service = app.emas['products_and_services'][sid]
            suids.append(IUUID(service))

    today = datetime.datetime.now().date()
    mids = []
    for brain in app.emas.portal_catalog.unrestrictedSearchResults(
            serviceuid=suids,
            portal_type='emas.app.memberservice',
            expiry_date={'query':  today, 'range':'min'}
            ):
        service = brain.getObject()
        if service.userid not in mids:
            mids.append(service.userid)


    total = len(mids)
    print '--------------------------------START-------------------------------'
    print 'Processing a total of %s members.' % total
    uids = utils.practice_service_uuids(portal)
    for count, mid in enumerate(mids):
        for subject in ['maths', 'science']:
            memberservices = utils.member_services_for_subject(portal,
                                                               uids,
                                                               mid,
                                                               subject)
            # group by grade
            d = {}
            for ms in memberservices:
                grade = ms.related_service.to_object.grade
                d.setdefault(grade, [])
                d[grade].append(ms)

            # now check for possible duplicates
            for grade, services in d.items():
                if len(services) <= 1:
                    continue
                else:
                    assert len(services) == 2
                    print 'Merging member services for member: %s' % mid
                    merge_memberservices(portal, services)
        
        if not count % 100:
            # Better commit the work too
            print 'Committing merges'
            transaction.commit()
    
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
