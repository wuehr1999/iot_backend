# iot_backend
Backend Software for collecting data of different IoT sensors

## POC: postgresql inside docker container and communication via python
this branch turns the example from https://sqlmodel.tiangolo.com/ alive.


the code is definitely not fancy yet but works.

```bash
# start database and rest api
docker-compose up --build -d

# in the browser, open following URL:
http://localhost:8000/docs

# play around with the CRUD endpoints

# stop database and rest api (state of database is persistent via mounted volume)
docker-compose down 
```


### TODO: 
#### A: 
the local folder 'postgres_data' is currently automatically created by docker-compose up and belongs user root.


when trying to rebuild the image with docker-compose up --build, docker will fail with error "cannot stat postgres_data..."


current workaround: just delete the folder with sudo rm -rf postgres_data and start docker-compose command again

#### B:
right now there is just one big main.py for the proof of concept.


in order to create a modular (pypi) packet, it is recommended to use a src layout with build backend provided by uv


please refer to the official uv docu for more info: https://docs.astral.sh/uv/concepts/projects/init/

```bash
uv init --python 3.14 --package .
```


