#!/bin/bash

psql -h 10.0.0.2 -U emas emas < update_memberserviceid_sequence.sql
