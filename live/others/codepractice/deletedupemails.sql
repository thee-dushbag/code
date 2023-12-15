drop table if exists person;

create table
  person (
    id int primary key auto_increment,
    email varchar(30) not null
  );

insert into
  person (email)
values
  ('simon@gmail.com'),
  ('faith@gmail.com'),
  ('njeri@gmail.com'),
  ('lydia@gmail.com'),
  ('njeri@gmail.com'),
  ('simon@gmail.com'),
  ('mark@gmail.com'),
  ('faith@gmail.com'),
  ('darius@gmail.com'),
  ('faith@gmail.com'),
  ('simon@gmail.com'),
  ('njeri@gmail.com'),
  ('faith@gmail.com');

select
  *
from
  person;

select
  *
from
  person
order by
  email desc,
  id;

delete from person
where
  id not in (
    select
      id
    from
      person
    group by
      email
    having
      id = min(id)
  );

select
  *
from
  person;