import os
import sys
import shutil
from types import NoneType, StringType, UnicodeType
from ordereddict import OrderedDict

import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds

EXPORT_PATH = os.path.join('scripts', 'memberservices.csv')
PREV_EXPORT_PATH = os.path.join('scripts', 'prev_export_memberservices.csv')

class RelationMarshaller(object):
    
    def marshall(self, relation):
        return str(relation.to_id)


class DateMarshaller(object):

    def marshall(self, date):
        if isinstance(date, StringType):
            return date
        return date.strftime('%d/%m/%Y')


class IntMarshaller(object):
    
    def marshall(self, raw_int):
        return str(raw_int)


MARSHALLERS = {'userid'          : None,
               'title'           : None,
               'related_service' : RelationMarshaller(),
               'expiry_date'     : DateMarshaller(),
               'credits'         : IntMarshaller(),
               'service_type'    : None,
              }
NAMES = \
    ['userid',
     'title',
     'related_service',
     'expiry_date',
     'credits',
     'service_type',
     ]


def getIgnoreList():
    ids = []
    try:
        prev_file = open(PREV_EXPORT_PATH, 'rb')
        content = prev_file.readlines()
        prev_file.close()
        for line in content:
            intid = int(line.split(',')[-1].strip('\r\n'))
            ids.append(intid)
    except IOError:
        print 'WARNING! File %s not found. Ignore list is empty!' % EXPORT_PATH
    return ids


def exportObject(item, portal):
    print 'Exporting object:%s' % item.getId()
    data = []
    for name in NAMES:
        value = getattr(item, name, '')
        marshaller = MARSHALLERS.get(name)
        if marshaller:
            value = marshaller.marshall(value)
        data.append(value)
    print data
    return ','.join(data), None


app = makerequest.makerequest(app)
portal = getattr(app, sys.argv[-1])

user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))
portal.setupCurrentSkin(portal.REQUEST)

export_file = open(EXPORT_PATH, 'wb')
# column headings
export_file.write('memberservice_id,' + ','.join(NAMES) + '\r\n')

# make a copy so we can compare against it on the next run
prev_file = open(PREV_EXPORT_PATH, 'a+b')

ignore_list = getIgnoreList()
intids = queryUtility(IIntIds, context=portal)
items = portal.memberservices.objectValues()
for counter, item in enumerate(items):
    number = str(counter+1)
    print 'Processing item %s of %s' % (number, len(items))
    print '----------------------------------------------'
    
    intid = intids.getId(item)
    if intid in ignore_list:
        print 'Skipping.'
        continue

    data, errors = exportObject(item, portal)

    if errors:
        print errors
    else:
        data = '%s,%s,%s\r\n' % (number, data, intid)
        export_file.write(data)
        prev_file.write(data)

export_file.close()
prev_file.close()

print 'Done'
print 'The file is available at:%s' % EXPORT_PATH
print '----------------------------------------------'
