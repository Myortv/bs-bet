CREATE TYPE bet_status AS ENUM ('pending', 'win', 'lose');

create table bet (
    id serial primary key,
    event_id int,
    bet_amount numeric(12, 2),
    status bet_status not null default 'pending'::bet_status
);
