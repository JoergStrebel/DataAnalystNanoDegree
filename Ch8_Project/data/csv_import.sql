
create table if not exists ontime (
  Year int,
  Month int,
  DayofMonth int,
  DayOfWeek int,
  DepTime  int,
  CRSDepTime int,
  ArrTime int,
  CRSArrTime int,
  UniqueCarrier varchar(5),
  FlightNum int ,
  TailNum varchar(8),
  ActualElapsedTime int,
  CRSElapsedTime int,
  AirTime int,
  ArrDelay int,
  DepDelay int,
  Origin varchar(3),
  Dest varchar(3),
  Distance int,
  TaxiIn int,
  TaxiOut int,
  Cancelled int,
  CancellationCode varchar(1),
  Diverted varchar(1),
  CarrierDelay int,
  WeatherDelay int,
  NASDelay int,
  SecurityDelay int,
  LateAircraftDelay int
);

truncate ontime;

\COPY ontime FROM '2005.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER, NULL 'NA');
\COPY ontime FROM '2006.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER, NULL 'NA');
\COPY ontime FROM '2007.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER, NULL 'NA');
\COPY ontime FROM '2008.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER, NULL 'NA');

-- calculated column flightdate; necessary as Tableau does not get it right.
alter table ontime add column flightdate date;
update ontime set flightdate = make_date(year,month, dayofmonth);


create table if not exists airports (
  iata varchar(10) primary key,
  airport  varchar(200),
  city  varchar(200),
  state  varchar(200),
  country varchar(200),
  lat decimal,
  long decimal
);

truncate airports;
\COPY airports FROM 'airports.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER, NULL 'NA');

create table if not exists carriers (
  code varchar(100) primary key,
  description  varchar(2000)
);

truncate carriers;
\COPY carriers FROM 'carriers.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER, NULL 'NA');

create table if not exists planes (
  tailnum varchar(100) primary key,
  type  varchar(2000),
  manufacturer  varchar(2000),
  issue_date  varchar(2000),
  model  varchar(2000),
  status  varchar(2000),
  aircraft_type  varchar(2000),
  engine_type  varchar(2000),
  year int
);

truncate planes;
\COPY planes FROM 'plane-data_corr.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER, NULL '');


--Statistiken aktualisieren lassen
Vacuum (analyze);

create index idx_year on ontime(year);
create index idx_date on ontime(year, month, dayofmonth);
create index idx_origin on ontime(origin);
create index idx_dest on ontime(dest);


