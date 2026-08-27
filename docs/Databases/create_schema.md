# Create Schema

In Postgres Schemas act as a logical namespace used to organize database objects like tables, views, indexes and functions. If a database is where you store your data, then a schema is a like a folder under which the data is filed. 

```sql
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
```