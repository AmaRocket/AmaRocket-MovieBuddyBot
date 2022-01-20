create table users
(
    id          serial,
    username    text,
    request     text,
);

alter table users
    owner to postgres;

create unique index users_id_uindex
    on users (id);