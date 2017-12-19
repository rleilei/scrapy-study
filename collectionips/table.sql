#创建数据库
CREATE DATABASE IF NOT EXISTS ips;
USE ips;
#创建表格

CREATE TABLE IF NOT EXISTS ips_tb(
	id INT KEY AUTO_INCREMENT ,
	ip CHAR(20) ,
	port CHAR(10),
	addrs VARCHAR(50),
	style CHAR(10),
	speed VARCHAR(20),
	alive_time CHAR(20),
	proof_time CHAR(29)
);