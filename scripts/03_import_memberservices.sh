#!/bin/bash

psql -h 10.0.0.2 -d emas -U emas < import_memberservices.sql
