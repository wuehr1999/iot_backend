# iot_backend

This project creates an univeral IoT backend, which can collect data from different WAN networks (TTN, ChripStack, custom solutions, ...).
For now, the data is concentrated in a PostgreSQL database and made available for further usage with an unified REST API.

## Installation (tested on Xubuntu 24.04)

### Setup PostgreSQL

~~~
sudo apt install postgresql
sudo -i -u postgres psql
ALTER USER postgres WITH PASSWORD 'postgres';
\q
~~~

### Install the Python package

~~~
python3 -m venv ./venv
source ./venv/bin/activate
git clone git@github.com:wuehr1999/iot_backend.git
cd iot_backend
pip3 install .
~~~

## Applications

### iot_backend_user_api

This application provides the unified REST API for data processing on ```Port 5000```. It can be tested with the Firefox plugin ```RESTer```.
~~~
source ./venv/bin/activate
iot_backend_user_api --help
Usage: iot_backend_user_api [OPTIONS]

Options:
  --host TEXT  Host IP address
  --help       Show this message and exit.
~~~

#### API endpoints

| Endpoint | Request | Description |
| -------- | ------- | ----------- |
| ```/temperature``` | | |
| | ```GET``` | Get the data of all temperature sensors. |
| | ```DELETE``` | Delete all temperature data. |

### iot_backend_ttn_storage

This application synchronizes the database to the TTN Application message storage.

~~~
source ./venv/vin/activate
iot_backend_ttn_storage --help
Usage: iot_backend_ttn_storage [OPTIONS]

Options:
  --application TEXT  Name of the TTN application  [required]
  --key TEXT          API key  [required]
  --interval INTEGER  Update interval in seconds
  --host TEXT         Host IP address
  --help              Show this message and exit.
~~~


# Roadmap

* [ ] Docker enviroment
* [ ] Define data formats for different sensor types
* [ ] Support different sensor types
* [ ] Define the featureset for the REST API
* [ ] MQTT connection to TTN
* [ ] Support TTN webhooks
* [ ] Consider security aspects for deployment on webservers
