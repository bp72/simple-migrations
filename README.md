# simple-migrations (beta)

[![PyPI version](https://img.shields.io/pypi/v/simple-migrations.svg)](https://pypi.org/project/simple-migrations)
[![Python versions](https://img.shields.io/pypi/pyversions/simple-migrations.svg)](https://pypi.org/project/simple-migrations)

### Please, notice that the library is early in the development, use it at your own risk. The feedback and contributions are appreciated!

Make your database migrations as simple as possible!

`simple-migrations` is a library that allows you to write database migrations in a pure SQL.

The order of migrations will be tracked in the database table.

You can specify the `forwards` and `backwards` command and even write your own scripts.

No need to apply the scripts manually, you can now automate your deployment flow!

Keep in mind that the library is still in development and is distributed "as is".

## How to use

The example of the config can be found in `simple_migrations.ini` file.

Create a `simple_migrations.ini` file in the project root and set up the database credentials.

Run `simple-migrations init` to generate the migrations directory and migrations table.

Run `simple-migrations generate` to generate the migration file from the template.

Run `simple-migrations migrate` to apply all unapplied migrations.

Run `simple-migrations migrate <num>` to migrate or rollback to <num> migration, for example:

- If the last applied migration was #2, `simple-migrations migrate 4` will apply migrations 3 and 4.
- If the last applied migration was #4, `simple-migrations migrate 2` will rollback migrations 3 and 4.
