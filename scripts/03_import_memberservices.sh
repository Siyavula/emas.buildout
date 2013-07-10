#!/bin/bash

psql -p 5435 -U emas emas < import_memberservices.sql
