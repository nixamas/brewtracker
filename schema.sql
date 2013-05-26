drop table if exists readings;
create table if not exists readings (
  id integer primary key autoincrement,
  reading_time text,
  reading_brew_temp text,
  reading_amb_temp text
);
