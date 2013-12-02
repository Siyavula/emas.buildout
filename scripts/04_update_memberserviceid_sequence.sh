#!/bin/bash

psql -p 5432 -U emas emas < update_memberserviceid_sequence.sql
