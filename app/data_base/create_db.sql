create table users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    id        serial            not null,
);

alter table users
    owner to telegram_db;

create unique index users_id_uindex
    on users (id);