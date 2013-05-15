drop table if exists readings;
create table if not exists readings (
  id integer primary key autoincrement,
  reading_time text not null,
  reading_brew_temp text not null,
  reading_amb_temp text not null
);
