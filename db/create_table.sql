"CREATE TABLE Logs (id_log integer primary key AUTOINCREMENT, remote_host varchar(15) default 'None', remote_logname varchar(50) default 'None', remote_user varchar(50) default 'None', request_line varchar(150) default 'None', final_status int default 0, bytes_sent int default 0, request_time timestamp with time zone UNIQUE default current_timestamp)"
-- create table Logs
-- (
-- 	id_log serial,
-- 	remote_host varchar(15) default 'None',
-- 	remote_logname varchar(50) default 'None',
-- 	remote_user varchar(50) default 'None',
-- 	request_line varchar(150) default 'None',
-- 	final_status int default 0,
-- 	bytes_sent int default 0,
-- 	request_time timestamp with time zone default UNIQUE current_timestamp 
-- );