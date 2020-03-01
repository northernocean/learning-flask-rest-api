delete from items;
delete from stores;
delete from users;

insert into stores (id, name) values (1, 'Store1');
insert into items (id, name, price, store_id) values (1, 'chair', 15.99, 1);
insert into users (id, username, password) values (1, 'david', 'password1');
insert into users (id, username, password) values (2, 'david2', 'password2');



