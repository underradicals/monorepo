# Create Database

## PSQL

### No `CREATE DATABASE` Inside a Transaction
The `CREATE DATABASE` DDL cannot run inside a Transaction and must run on its own. Unlike other DDL like `CREATE TABLE` or `ALTER TABLE` the `CREATE DATABASE` command access the internals of Postgres on a deeper level.

### What happens when we run `CREATE DATABASE`
Creating a database is not like adding a row to a table. It must access the file system to copy a complete template database called `template1`. This coping of the template database is not trivial because Postgres must fork a background process to physically duplicate the files it needs and it must register the new directory with the OS. The OS does not provide a native `"rollback"` feature. So if ran a `CREATE DATABASE` inside a transaction next to other commands and one of those commands failed, Postgres would have to begin a complex and error prone manual cleanup of the physical file system while also ensuring that no files were locked or destroyed or corrupted. 

### So why not just use `IF NOT EXISTS`
Postgres has a systems catalog that is global across the entire instance of Postgres. If we were to run `CREATE DATABASE` inside a transaction we would need to require a lock on those system catalog tables which would prevent other users across the cluster from accessing the system catalog. 


### The Work Around
```sql
SELECT FORMAT(
    'CREATE DATABASE %I WITH OWNER %I '
    'ENCODING ''UTF8'' LOCALE_PROVIDER = ''libc'' '
    'CONNECTION LIMIT -1 IS_TEMPLATE = false', 
    'd2', 
    'postgres'
) 
WHERE NOT EXISTS (
    SELECT 1 FROM pg_database WHERE datname = 'd2'
)\gexec
```