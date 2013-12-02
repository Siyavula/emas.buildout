Stop all instances on siyavula p02 and p03 PLUS both zeoservers
---------------------------------------------------------------

    On siyavula p02, look for:
    ./bin/primary-zeo

    And on siyavula p03 look for:
    ./bin/secondary-zeo

    Instances should be at:
    ./bin/instance[1-4] on both siyavula p02 and p03.

Get the latest filestorage and blobstorage from siyavula3
---------------------------------------------------------
    
    In [instance home]/var, execute:

    rsync --bwlimit=10000 -Pva --rsh="ssh -p222" siyavula3.upfronthosting.co.za:/home/zope/instances/emas.buildout/var/filestorage ./filestorage

    rsync --bwlimit=10000 -Pva --rsh="ssh -p222" siyavula3.upfronthosting.co.za:/home/zope/instances/emas.buildout/var/blobstorage ./blobstorage

    Both these will take some time so watch the progress and 'top' on s3.

Restart both zeoservers on sp02 and sp03
----------------------------------------

Clear the existing memberservices from the database
---------------------------------------------------

    On siyavula p02 access the database with:
    >>psql -h 10.0.0.2 -d emas -U emas

    At the postgresql prompt "emas=>" use:
    \d
    to get a list of all the tables in the 'emas' database.

    Clear the memberservices table with:
    DELETE from memberservices;

    This might take a while depending on then current amount of rows. 
    
    Reset the sequence "memberservices_memberservice_id_seq" with:
    ALTER SEQUENCE memberservices_memberservice_id_seq RESTART with 1;

Export current memberservices
-----------------------------

    In [instance]/scripts run:
    ./bin/instance1 run ./scripts/01_export_memberservices.py emas

    We currently have more than 210000 memberservices so this process runs for
    a bit.

    This proces will create a file at ./scripts/memberservices.csv

Import memberservices to postgres DB
------------------------------------
    
    In [instance]/scripts run:
    ./03_import_memberservices.sh

    NB: check the memberservices_memberservice_id_seq sequence. Make sure it
    is set to a value greater than:
    select max(memberservice_id) from memberservices;
    
    To set the sequence value use:
    alter sequence memberservices_memberservice_id_seq restart with NNN;

Update the memberserviceid sequence
-----------------------------------
    
    Edit [instance]/scripts/update_memberserviceid_sequence.sql
    Change the restart value to the max of memberserviceid in the memberservices
    table.
    You can get the value in a psql session with something like this:
    select max(memberservice_id) from memberservices;
    
    In [instance]/scripts run:
    ./04_update_memberserviceid_sequence.sh


Delete old memberservices
-------------------------

    In [instance]/scripts run:
    ./05_delete_old_memberservices.py emas

    Be patient this will take quite some time.
