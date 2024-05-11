Setting Up the Environment and implementation
1. React Frontend Initialization (You need to have Node.js installed).Install create-react-app globally
```
npm install -g create-react-app
```
```
npm install reactstrap react react-dom
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
10. TimescaleDB Setup , You need to have Docker installed for running TimescaleDB.
```
docker pull timescale/timescaledb:latest-pg12
```
11. Run a TimescaleDB instance
```
docker run -d --name timescale -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12
```
