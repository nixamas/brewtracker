create table if not exists readings (
  id integer primary key autoincrement,
  reading_time text,
  reading_brew_temp text,
  reading_amb_temp text
);

create table if not exists mybeer (
  id integer primary key autoincrement,
  name text,
  ingredients text,
  brew_date text,
  second_stage_date text,
  bottle_date text,
  abv text,
  volume_brewed text,
  notes text
);

create table if not exists gravity_readings (
  brew_id integer DEFAULT '-1',
  id integer DEFAULT '-1',
  gravity_reading_time text,
  gravity_reading text
);