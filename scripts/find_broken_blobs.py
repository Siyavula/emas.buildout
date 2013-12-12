"""
    A Zope command line script to report content with missing BLOB in Plone, causing
    POSKeyErrors when content is being accessed or during portal_catalog rebuild.

    Tested on Plone 4.1 + Dexterity 1.1.

    http://stackoverflow.com/questions/8655675/cleaning-up-poskeyerror-no-blob-file-content-from-plone-site

    Also see:

    http://pypi.python.org/pypi/experimental.gracefulblobmissing/

"""

import sys
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

# Zope imports
from zope.app.component.hooks import setSite
from ZODB.POSException import POSKeyError
from zope.component import getMultiAdapter
from zope.component import queryUtility
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFCore.interfaces import IFolderish, ISiteRoot

# Plone imports
from five import grok
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Field import FileField
from Products.Archetypes.interfaces import IBaseContent
from plone.namedfile.interfaces import INamedFile
from plone.dexterity.content import DexterityContent


def check_at_blobs(context, report_file):
    """ Archetypes content checker.

    Return True if purge needed
    """
    if IBaseContent.providedBy(context):
        schema = context.Schema()
        for field in schema.fields():
            id = field.getName()
            if isinstance(field, FileField):
                try:
                    field.get_size(context)
                except POSKeyError:
		    msg = "Found damaged AT FileField %s on %s" % (id, context.absolute_url())
		    report_file.write(msg)
                    print msg
                    return True

    return False


def check_dexterity_blobs(context, report_file):
    """ Check Dexterity content for damaged blob fields

    XXX: NOT TESTED - THEORETICAL, GUIDELINING, IMPLEMENTATION

    Return True if purge needed
    """
    # Assume dexterity contennt inherits from Item
    if isinstance(context, DexterityContent):
        # Iterate through all Python object attributes
        # XXX: Might be smarter to use zope.schema introspection here?
        for key, value in context.__dict__.items():
            # Ignore non-contentish attributes to speed up us a bit
            if not key.startswith("_"):
                if INamedFile.providedBy(value):
                    try:
                        value.getSize()
                    except POSKeyError:
			msg = "Found damaged Dexterity plone.app.NamedFile %s on %s" % (key, context.absolute_url())
                        print msg
			report_file.write(msg)
                        return True
    return False


def report_objects_with_broken_blobs(context, report_file):
    """
    Iterate through the object variables and see if they are blob fields
    and if the field loading fails then poof
    """
    if check_at_blobs(context, report_file) or check_dexterity_blobs(context, report_file):
        print "Bad blobs found on %s" % context.absolute_url()


def recurse(tree, report_file):
    """ Walk through all the content on a Plone site """
    print 'Checking %s' % tree.getId()
    for id, child in tree.contentItems():
	report_objects_with_broken_blobs(child, report_file)
        if IFolderish.providedBy(child):
            recurse(child, report_file)



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

report_file = open('broken_blobs.txt', 'wb')
print "Checking blobs"
recurse(portal, report_file)
report_file.close()
print "All done"
