drop table if exists user;
create table user (
  user_id int AUTO_INCREMENT,
  username varchar(255) not null,
  email varchar(255) not null,
  pw_hash varchar(255) not null,
  PRIMARY KEY (user_id)
);

drop table if exists follower;
create table follower (
  who_id int,
  whom_id int,
  PRIMARY KEY (who_id, whom_id)
);

drop table if exists message;
create table message (
  message_id int AUTO_INCREMENT,
  author_id int not null,
  text varchar(255) not null,
  pub_date TIMESTAMP,
  flagged int,
  PRIMARY KEY (message_id)
);
