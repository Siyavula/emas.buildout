#!/bin/bash

psql -p 5435 -U emas emas < update_memberserviceid_sequence.sql
