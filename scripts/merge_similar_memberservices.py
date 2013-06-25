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
    now = datetime.datetime.now().date()
    delta = other.expiry_date - now
    if delta.days > 0:
        self.expiry_date = self.expiry_date + delta
    self_subs_period = self.related_service.to_object.subscription_period
    other_subs_period = other.related_service.to_object.subscription_period
    if other_subs_period > self_subs_period:
        self.related_service = other.related_service
    return self


def merge_memberservices(portal, memberservices, current_idx=0):
    if not memberservices or current_idx >= len(memberservices):
        return memberservices

    other = memberservices[current_idx]
    for memberservice in memberservices:
        if memberservice == other:
            continue
        if is_similar_to(memberservice, other):
            print '    %s and %s are similar, merging...' % (
                memberservice.Title(), other.Title()
            )
            merge_with(memberservice, other)
            portal.memberservices.manage_delObjects([other.getId()])
    return merge_memberservices(portal, memberservices, current_idx+1) 


def process(portal, pmt, merged):
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
            titles = [ms.Title() for ms in memberservices]
            if len(memberservices) <= 1:
                continue

            print 'Merging member services for member: %s' % mid
            merge_memberservices(portal, memberservices)
            tmpservices = merged.get(mid, [])
            tmpservices.extend(titles)
            merged[mid] = tmpservices
        
        if not count % 100:
            # Better commit the work too
            print 'Commit 100 merges now.'
            transaction.commit()
    
    return merged
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
merged = {}
merged = process(portal, pmt, merged)

print '-------------------------------------------------------------------'
print "The following %s members services where merged:" % len(merged)
for mid, titles in merged.items():
    print '%s\r' % mid

