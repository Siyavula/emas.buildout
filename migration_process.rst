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


Create MEMBERSERVICE table
--------------------------

Extract memberservices as CSV
-----------------------------

    In the top level dir of the relevant zope instance run:
    ./bin/instance run ./scripts/export_memberservices.py emas


Import memberservices to postgres DB
------------------------------------

Delete old memberservices
-------------------------

Remove memberservice content type, workflows, etc.
--------------------------------------------------

Delete old memberservices folder
--------------------------------
