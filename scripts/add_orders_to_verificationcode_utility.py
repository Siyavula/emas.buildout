import sys
import datetime
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from ZODB.POSException import ConflictError
from zope.app.component.hooks import setSite
from zope.component import getUtility

from emas.app.utilities import IVerificationCodeUtility
from emas.app.order import Order

from logging import getLogger

TIME_FORMAT = '%H:%M:%S:%s'


def process(portal):
    print '-------------------------------------------------------------------'
    print('Started at:%s' % datetime.datetime.now().strftime(TIME_FORMAT))
    vcu = getUtility(IVerificationCodeUtility, context=portal)
    for count, order in enumerate(portal.orders.objectValues()):
        try:
            if order.verification_code:
                print('Adding order:%s number%s' % (order.getId(), count))
                vc = int(order.verification_code)
                if vcu.is_unique(vc):
                    vcu.add(vc, order)
                else:
                    print 'Duplicate verification code:%s for order:%s' % (vc, order.getId())
                    new_vc = vcu.generate(order)
                    order.verification_code = new_vc
                    order.reindexObject(idxs=['verification_code'])
        except ConflictError as e:
            print 'Could not add order:%s' % order.getId()
        if not count % 1000:
            transaction.commit()
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
