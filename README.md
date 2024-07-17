Setting Up the Environment and implementation
1. React Frontend Initialization (You need to have Node.js installed).Install create-react-app globally
```
npm install -g create-react-app
```
```
npm install axios
```

```
npm install --save @chakra-ui/react
```

2. Create a new React app named "network-monitoring-frontend"
```
create-react-app network-monitoring-frontend
```
3. Navigate into your newly created app
```
cd network-monitoring-frontend
```
4. Start the development server
```
npm start
```
5. Django Backend Initialization . Install Django and djangorestframework
```
pip install django djangorestframework
```
6. Create a new Django project named "network_monitoring_backend"
```
django-admin startproject network_monitoring_backend
```
7. Navigate into your Django project
```
cd network_monitoring_backend
```
8. Create a new Django app named "api"
```
python manage.py startapp api
```
9.Start the development server
```
python manage.py runserver
```
10. Install PostgreSQL first and config it . (default user = postgres database = postgres)
```
pip install psycopg2
```
11. TimescaleDB Setup , You need to have Docker installed for running TimescaleDB.
```
docker pull timescale/timescaledb:latest-pg12
```
12. Run a TimescaleDB instance
```
docker run -d --name timescale -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12
```
13. make hypertable for usuing TimescaleDB (use this command in psql shell)
```
psql -U postgres -d postgres
```
```
create_hypertable('app_devicedata', 'timestamp');
```
We have two sets of data a mock data that we generate and a snmp data that the app will collect. we trained the AI on a mock data so we can find anomaly in the data that we have in this case RAM and CPU usage.

Our mock data for training have 130000 data that we made up and from this data 100000 is clean data without anomaly and 30000 of it with anomaly and we train them with labels and get 91% accuracy out of it.

After we train our model we make use of it in our backend and connect it to the websocket so we can have realtime data like cpu and ram usuage , just first the ram and cpu usage will be made and base on them the model will predict if they have anomaly or not

The anomaly in the data is made of three different anomaly that it get trained on

1 - ram usage more than 90% and cpu usage less than 20%

2 - cpu usage more than 90% and ram usage less than 20%

3 - ram usage more than 90% and cpu usage more than 90%
