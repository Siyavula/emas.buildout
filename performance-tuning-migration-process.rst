Create new cluster and database
-------------------------------
    
    Create a new 9.1 cluster
    pg_createcluster emas

    Become the postgres user
    >>sudo -i -u postgres

    Access the database
    >>psql -p 5435 (NB: check on which PORT the RELEVANT CLUSTER runs!)
    
    Create the new database
    create database emas;

    Create the emas database user
    create user emas with password 'emas';

    Give the user the necessary rights
    grant all privileges on database emas to emas;

    edit /etc/postgres/9.1/emas/pg_hba.conf                                
    add the following:                                                      
    local   emas     emas                           trust 

    Access the DB as emas user
    >>psql -p 5435 -U emas

Set max_prepared_transactions
-----------------------------

    We are using two-phased commits, so we cannot operate with 0 
    max_prepared_transactions. It causes and OperationalError.
    
    Set max_prepared_transactions to something greater than 0 and preferably to
    the same value as max_connections.

    This is done in:
    /etc/postgresql/9.1/emas/postgresql.conf
    
    Restart postgres:
    /etc/init.d/postgresql restart

    If the restart fails you might have to check the kernel's SHMMAX parameter.

Export current memberservices
-----------------------------

    In [instance]/scripts run:
    ./bin/instance run ./scripts/01_export_memberservices.py emas

Create MEMBERSERVICE table
--------------------------

    In [instance]/scripts run:
    ./02_create_memberservices_table.sh

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

Install monassis
----------------

    pg_createcluster 9.1 monassis

