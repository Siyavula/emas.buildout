#!/bin/bash

psql -p 5432 -U emas emas < import_memberservices.sql
