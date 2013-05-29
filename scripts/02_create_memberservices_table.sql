CREATE TABLE MEMBERSERVICES (
    MEMBERSERVICE_ID serial primary key,
    USERID varchar(100) not null,
    RELATED_SERVICE integer not null,
    EXPIRY_DATE date,
    CREDITS integer,
    SERVICE_TYPE varchar(100)
);
