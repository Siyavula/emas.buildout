CREATE TABLE MEMBERSERVICES (
    MEMBERSERVICE_ID serial primary key,
    MEMBERID varchar(100) not null,
    TITLE varchar(100) not null,
    RELATED_SERVICE_ID integer not null,
    SUBJECT varchar(100) not null,
    GRADE varchar(100) not null,
    EXPIRY_DATE date,
    CREDITS integer,
    SERVICE_TYPE varchar(100),
    ZOPE_UID integer unique
);
