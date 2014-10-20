Create new cluster and database
-------------------------------
    
    Create a new 9.1 cluster
    pg_createcluster emas

    Become the postgres user
    >>sudo -i -u postgres

    Access the database
    >>psql -p 5432 (NB: check on which PORT the RELEVANT CLUSTER runs!)
    
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
    >>psql -p 5432 -U emas

    On siyavula p02 this won't work, rather use:
    >>psql -h 10.0.0.2 -d emas -U emas

    To get a list of all the tables in the 'emas' database at the postgresql
    prompt "emas=>" use:
    \d

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

Create MEMBERSERVICE table
--------------------------

    In [instance]/scripts run:
    ./02_create_memberservices_table.sh

Install monassis
----------------
