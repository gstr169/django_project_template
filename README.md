This project use .env file for storing some settings. 

Example stored in you_need.env

You can build project with default settings, without .env

If you builded project without .env, and after created .env, your settings will not be applied.

To apply settings, you will need rebuild project.

You can rebuild project with `docker-compose up -d --build`

If you changed database settings in .env, you will remove volume with database data.

You can do it by `docker-compose down -v`

### Settings list:

`PGPASSWORD=postgres` - password for user `postgres`

`PGDATABASE=postgres` - database name where django will store data

`WORKERS=1` - amount of gunicorn workers _(by default - amount of cpu cores)_

`APP_ENV=devel` - environment setting _(prod or dev/devel/developer)_
