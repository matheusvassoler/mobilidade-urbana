-- Database: "hazard-mobility"

-- DROP DATABASE "hazard-mobility";

CREATE DATABASE "hazard-mobility"
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

drop table if exists distances_sjc_sp;

--SJC_SP

CREATE TABLE public.distances_sjc_sp
(
  id serial primary key,
  idx_origin character varying(1000),
  idx_destination character varying(1000),
  origin character varying(1000),
  destination character varying(1000),
  distance_meters character varying(1000),
  mode character varying(1000),
  path text,
  duration character varying(1000),
  intermediate_paths_ok character varying(1000),
  processed int
);

delete from distances_sjc_sp;



DROP TABLE if exists intermediate_distances_sjc_sp;

CREATE TABLE public.intermediate_distances_sjc_sp
(
  id serial primary key,
  id_distances_sjc_sp character varying(1000),
  duration_seconds character varying(1000),
  start_point character varying(1000),
  end_point character varying(1000),
  mode character varying(1000),
  path text,
  distance_meters character varying(1000),
  processed int
);

delete from intermiate_distances_sjc_sp;

--SJC_SP WHEN

CREATE TABLE public.distances_sjc_sp_when
(
  id serial primary key,
  idx_origin character varying(1000),
  idx_destination character varying(1000),
  origin character varying(1000),
  destination character varying(1000),
  distance_meters character varying(1000),
  mode character varying(1000),
  path text,
  duration character varying(1000),
  intermediate_paths_ok character varying(1000),
  processed int,
  whentime character varying(1000)
);

CREATE TABLE public.intermediate_distances_sjc_sp_when
(
  id serial primary key,
  id_distances_sjc_sp character varying(1000),
  duration_seconds character varying(1000),
  start_point character varying(1000),
  end_point character varying(1000),
  mode character varying(1000),
  path text,
  distance_meters character varying(1000),
  processed int
);


--RMRJ_RJ

CREATE TABLE public.distances_rmrj_rj
(
  id serial primary key,
  idx_origin character varying(1000),
  idx_destination character varying(1000),
  origin character varying(1000),
  destination character varying(1000),
  distance_meters character varying(1000),
  mode character varying(1000),
  path text,
  duration character varying(1000),
  intermediate_paths_ok character varying(1000),
  processed int
);

CREATE TABLE public.intermediate_distances_rmrj_rj
(
  id serial primary key,
  id_distances_rmrj_rj character varying(1000),
  duration_seconds character varying(1000),
  start_point character varying(1000),
  end_point character varying(1000),
  mode character varying(1000),
  path text,
  distance_meters character varying(1000),
  processed int
);

--RMRJ_RJ When

CREATE TABLE public.distances_rmrj_rj_when
(
  id serial primary key,
  idx_origin character varying(1000),
  idx_destination character varying(1000),
  origin character varying(1000),
  destination character varying(1000),
  distance_meters character varying(1000),
  mode character varying(1000),
  path text,
  duration character varying(1000),
  intermediate_paths_ok character varying(1000),
  processed int,
  whentime character varying(1000)
);

CREATE TABLE public.intermediate_distances_rmrj_rj_when
(
  id serial primary key,
  id_distances_rmrj_rj character varying(1000),
  duration_seconds character varying(1000),
  start_point character varying(1000),
  end_point character varying(1000),
  mode character varying(1000),
  path text,
  distance_meters character varying(1000),
  processed int
);

