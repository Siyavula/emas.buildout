CREATE TABLE MEMBERSERVICES (
    MEMBERSERVICE_ID integer primary key not null,
    USERID varchar(100) not null,
    RELATED_SERVICE integer not null,
    EXPIRY_DATE date not null,
    CREDITS integer,
    SERVICE_TYPE varchar(100)
);
