Introduction
============

This package contains the buildout configuration for the Everything
Maths & Science Plone sites.

Dependencies
============

Assuming you are on a deb based distribution, you need to install the
following packages:

    build-essential python2.6 python2.6-dev libpng12-dev zlib1g-dev
    libfreetype6-dev libjpeg62-dev libxml2-dev libbz2-dev
    libreadline-dev python-virtualenv

Installation
============

The installation steps below are for development purposes only.

1. First clone the buildout from github:

    git clone git@github.com:rochecompaan/emas.buildout.git emas.buildout

2. Change into emas.buildout and create a virtualenv:

    cd emas.buildout
    virtualenv -p /usr/bin/python2.6 --no-site-packages . 

3. Bootstrap and run buildout:

    bin/python boostrap -c dev.cfg
    bin/buildout -c dev.cfg

    WARNING: This will take a long time since it downloads Plone, Zope
    and all the packages required by it to run.

4. Start Plone in the foreground:

    bin/instance fg

5. Browse to http://localhost:8080 and click on "Create a new Plone site".
   Select "emas.theme" from the list of Add-ons and click on "Create
   Plone Site". This add-on will install all the dependent add-ons
   required by the theme.
