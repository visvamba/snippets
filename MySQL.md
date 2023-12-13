# MySQL snippets

### Log in to local instance

```bash
mysql -u <user> -p
```

### Creating database

```mysql
CREATE DATABASE IF NOT EXISTS <db_name>;
```

### Create table

```mysql
CREATE TABLE <table_name> (
	id INT,
	<columnname> <columntype>,
	PRIMARY KEY(id)
);
```

### Delete table

```mysql
DROP TABLE IF EXISTS <table_name>;
```



### Switch to DB

```mysql
USE <db_name>
```

## Users

### Grant user privileges on a DB

```mysql
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';
```



## Export DB

### Whole DB

```bash
mysqldump -h <host> --port=<port> -u <user> -p <DB name> > <output file>.sql
```

### Schema only

```bash
mysqldump -h <host> --port=<port> -u <user> -p --no-data <DB name> > <output file>.sql
```

### A table

```bash
mysqldump -h <host> --port=<port> -u <user> -p --no-data <DB name> <table name> > <output file>.sql
```

### Import

```bash
mysql -u <user> -p <new db name> < <exported>.sql
```





UPDATE *table_name*
SET *column1* = *value1*, *column2* = *value2*, ...
WHERE *condition*; treat
