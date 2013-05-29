import os
import sys
from types import NoneType, StringType, UnicodeType
from ordereddict import OrderedDict

import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName

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


MARSHALLERS = {'userid': None,
               'related_service': RelationMarshaller(),
               'expiry_date': DateMarshaller(),
               'credits': IntMarshaller(),
               'service_type': None,
              }
NAMES = \
    ['userid', 'related_service', 'expiry_date', 'credits', 'service_type']


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

path = os.path.join('scripts', 'memberservices.csv')
export_file = open(path, 'wb')
# column headings
export_file.write(','.join(NAMES) + '\r\n')

items = portal.memberservices.objectValues()
for counter, item in enumerate(items):
    print 'Processing item %s of %s' % (counter+1, len(items))
    print '----------------------------------------------'
    
    data, errors = exportObject(item, portal)

    if errors:
        print errors
    else:
        export_file.write(data + '\r\n')

export_file.close()

print 'Done'
print 'The file is available at:%s' %path
print '----------------------------------------------'
