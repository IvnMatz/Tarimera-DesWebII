-- PASOS PARA CONFIGURAR LA BASE DE DATOS

-- CREA LA BASE
create database UsersWebP

--USE 
use UsersWebP

--TABLAS
create table users(
id_user int not null primary key,
username varchar(50) not null,
passw varchar(20) not null,
mail varchar(100) not null,
theme int not null);
-- ### ANOTACIÓN DE USERS: siempre el usuario de ID 0 será admin, por lo que eso, tomalo en cuenta

create table products(
id_product int not null primary key,
nombre varchar(50) not null,
price int not null,
descript varchar(100) not null,
dimension varchar(30) not null,
peso int not null);

create table saved_product(
id_user int not null,
id_product int not null);

create table review(
id_review int not null primary key,
title varchar(30) not null,
descript varchar(100) not null,
calif int not null,
id_user int not null,
id_product int not null);

