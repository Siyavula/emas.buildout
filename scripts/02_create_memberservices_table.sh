#!/bin/bash

psql -p 5432 -U emas emas < create_memberservices_table.sql
psql -p 5432 -U emas emas < add_indexes.sql
