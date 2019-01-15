create table if not exists LoadFile(
    filename text primary key,
    mtime    int
);

create table if not exists PaymentData(
    subno   text,
    at      text,
    ac      text,
    "in"    text,
    dn      text,
    vv      real,
    vv2     real,
    primary key(subno,at,ac,in,dn)
);

