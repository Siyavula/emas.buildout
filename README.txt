Introduction
============

This package contains the buildout configuration for the Everything
Maths & Science Plone sites.

Dependencies
============

Assuming you are on a deb based distribution, you need to install the
following packages:

    build-essential python2.6 python2.6-dev libpng12-dev zlib1g-dev
    libfreetype6-dev libjpeg62-dev libxml2-dev libxslt1-dev libbz2-dev
    libreadline-dev python-virtualenv libxrender1 libfontconfig1 dvipng
    texlive-latex-base ttf-freefont imagemagick

Tralics needs to be installed manually and put anywhere on your path:

    Download the tarbal from:

        ftp://ftp-sop.inria.fr/apics/tralics-src/tralics-src-2.14.4.tar.gz
    
    Extract the tarbal, run make and then copy the tralics binary to
    /usr/local/bin

Install wkhtmltoimage by downloading the binary from:

    http://code.google.com/p/wkhtmltopdf/downloads/list

    Extract the tarball, rename the binary to wkhtmltoimage and move it
    to /usr/local/bin.


Installation
============

The installation steps below are for development purposes only.

0. Create and change to a local user for running the Plone site (don't
   run as root).

1. First clone the buildout from github:

    git clone git@github.com:Siyavula/emas.buildout.git emas.buildout

2. Change into emas.buildout and create a virtualenv:

    cd emas.buildout
    virtualenv -p /usr/bin/python2.6 --no-site-packages . 

3. Bootstrap and run buildout:

    bin/python bootstrap.py -c dev.cfg
    bin/buildout -c dev.cfg

    WARNING: This will take a long time since it downloads Plone, Zope
    and all the packages required by it to run.

4. Start Plone in the foreground:

    bin/instance fg

5. Browse to http://127.0.0.1:8080 and click on "Create a new Plone site".

6. Enter "admin/admin" as username and password when prompted.

7. Select "emas.theme" from the list of Add-ons and click on "Create
   Plone Site". This add-on will install all the dependent add-ons
   required by the theme. 
   
8. You should now see a page title "Welcome to Plone" with 
   "Congratulations! You have successfully installed Plone." as
   description. To see the themed version of the site you can browse to
   http://localhost:8080/Plone. NOTE: the theme is still incomplete and
   under development.

How to add cnxmlplus files through the web
==========================================

1. Add a new "XML File" using the "Add New" drop down menu (on the
   right, between the "Display" and "State" menus.

2. Enter the title of the file and change the XML Format to
   "application/cnxmlplus+xml"

3. Copy and paste the xml content of cnxmlplus file into the text area

4. Save the form.

5. You should now see the HTML version of the page.

How to add cnxml/cnxmlplus files using FTP
====================================

1. Use a FTP client to connect to localhost on port 8021

2. Upload a file with "cnxmlplus" as extension eg index.cnxmlplus to
create an xml file inside Plone with "application/cnxmlplus+xml" as XML
Format.

3. Upload a file with "cnxml" as extension eg index.cnxml to create an
xml file inside Plone with "application/cnxml+xml" as XML Format.

Where are the transforms located and how do they work
=====================================================

CNXMLPlus files are transformed using a chain of transforms. First
cnxmlplus is converted to cnxml with embedded shortcodes, then cnxml
is converted to shortcodehtml and finally shortcodehtml is converted
to html.

Inside your buildout there is a "src" directory which contains the
emas.theme package. The transforms are located in the transforms
directory:

    src/emas.theme/emas/theme/transforms

The unit tests for transforms are located in the tests package:

    src/emas.theme/emas/theme/tests/test_transforms.py

Unit tests can be run using the bin/test command. The following command
wil run all tests in the emas.theme package.

    bin/test -s emas.theme

If you want to run a specific test you can specify the name of test
using the "-t" switch:

    bin/test -s emas.theme -t TestTranforms

Using git pre-commit hook script
================================

    cd .git/hooks
    ln -s ../../pre-commit.py pre-commit
    chmod +x pre-commit
