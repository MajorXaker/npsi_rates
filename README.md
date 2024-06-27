# NBRB Rates collector

A family of services to collect rates data from National Bank of Belarus. 

This system consists of 3 modules to perform operations of collecting data, storing data in database and sending the data to end users:
- Core. Module which tracks timetable, sends tasks on WORKER, stores data in PGSQL.
- WORKER. Module to perform various time-consuming tasks: download rates using NBRB API, send emails with CSV data on collected rates.
- API. Module with REST API access to database data and configs.


# Install and run
- Create docker-compose.yml with the following content
```yaml
version: '2'

services: 
  api:
    container_name: nbrb_api
    image: ghcr.io/majorxaker/npsi_rates:main
    env_file:
      - ./.env
    ports:
      - "8000:8000"

  core:
    container_name: nbrb_core
    image: ghcr.io/majorxaker/npsi_rates/core:main
    env_file:
      - ./.env
  
  worker:
    container_name: nbrb_worker
    image: ghcr.io/majorxaker/npsi_rates/worker:main
    env_file:
      - ./.env
```
- (optional) Add launch options for RabbitMQ and Postgres to your docker-compose file. Attach correct environment variables
- Create .env file for api and worker, replace asterisks with your values
```yaml
#PGSQL database credentials
DATABASE_USER=***
DATABASE_PASSWORD=***
DATABASE_DB=***
DATABASE_HOST=***
#rabbitmq parameters for Celery
RABBITMQ_USERNAME=***
RABBITMQ_PASSWORD=***
#parameters for email system
SMTP_SERVER=***
SMTP_PORT=***
SMTP_LOGIN=***
SMTP_PASSWORD=***
WEB_LOGIN=***
WEB_PASSWORD=***
```
- Pull, build and launch containers
```shell
docker-compose up -d
```
- Enter API container and run alembic migration to create tables in DB
```shell
docker container <container_id> exec bash
alembic upgrade head
 ```
- (optionally) Configure your reverse proxy to make API available from outside
- Send POST to /config to initiate whole system. See /docs endpoint to get more information on schema
- Send POST to /email_recipients to add an email to mailing list
- Enjoy your daily rates!