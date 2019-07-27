-- auto-generated definition
create table resource_categories
(
  id         serial       not null
    constraint resource_categories_pkey
    primary key,
  name       varchar(255) not null,
  short_name varchar(255) not null
);

alter table resource_categories
  owner to postgres;



-- auto-generated definition
create table resource_types
(
  id          serial       not null
    constraint resource_types_pkey
    primary key,
  name        varchar(255) not null,
  short_name  varchar(255) not null,
  category_id integer
    constraint resource_types_category_id_fkey
    references resource_categories
);

alter table resource_types
  owner to postgres;


-- auto-generated definition
create table resources
(
  id              serial      not null
    constraint resources_pkey
    primary key,
  type_id         integer
    constraint resources_type_id_fkey
    references resource_types,
  name            varchar(255),
  status          varchar(10) not null,
  donated_by_id   integer
    constraint resources_donated_by_id_fkey
    references users,
  taken_by_id     integer
    constraint resources_taken_by_id_fkey
    references users,
  requested_by_id integer
    constraint resources_requested_by_id_fkey
    references users,
  created_at      timestamp
);

alter table resources
  owner to postgres;




-- auto-generated definition
create table users
(
  id           serial       not null
    constraint users_pkey
    primary key,
  phone_number varchar(20)  not null,
  name         varchar(255) not null,
  email        varchar(255) not null,
  sex          varchar(5),
  user_type    varchar(20)  not null,
  dob          date,
  user_class   varchar(20),
  school       varchar(255),
  created_at   timestamp,
  address      varchar(255) not null
);

alter table users
  owner to postgres;

