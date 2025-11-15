\c tickets

\c flights

insert into airport(name,city,country) values ('Шереметьево', 'Москва', 'Россия'),('Пулково', 'Санкт-Петербург', 'Россия');

insert into flight(flight_number,datetime,from_airport_id,to_airport_id,price) values (
    'AFL031',
    '2021-10-08 20:00',
    (select id from airport where name = 'Пулково'),
    (select id from airport where name = 'Шереметьево'),
    1500
);

\c privileges

INSERT INTO privilege (username, status, balance)
VALUES ('test_user', 'BRONZE', 1000);