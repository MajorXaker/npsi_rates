# NBRB Rates collector

A family of services to collect rates data from National Bank of Belarus. 

This system consists of 3 modules to perform operations of collecting data, storing data in database and sending the data to end users:
- Core. Module which tracks timetable, sends tasks on WORKER, stores data in PGSQL.
- WORKER. Module to perform various time-consuming tasks: download rates using NBRB API, send emails with CSV data on collected rates.
- API. Module with REST API access to database data and configs.


# Installation and first launch
### Quick way:
- Use pre-made docker-compose.yml, to launch services locally.
```shell
docker-compose up
```
### Advanced way:
- Edit the provided docker-compose.yml to meet your specific needs.
- (Optional) Enter API container and run alembic migration to create tables in DB, if you have not specified it in docker-compose.
```shell
docker container <container_id> exec bash
alembic upgrade head
 ```
- (optionally) Configure your reverse proxy to make API available from outside

# Initial configs
- Send POST to /config to initiate whole system. See /docs endpoint to get more information on schema
- Send POST to /email_recipients to add an email to mailing list
- Enjoy your daily rates!