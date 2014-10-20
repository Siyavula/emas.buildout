SET datestyle = "ISO, DMY";
\copy MEMBERSERVICES FROM './memberservices.csv' DELIMITER ',' CSV HEADER;
