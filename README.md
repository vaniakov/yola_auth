# Users REST-service

## Installation
```bash
git clone https://github.com/vaniakov/yola_auth.git
cd yola_auth
python3 -m pip install virtualenv
mkdir -p ~/.virtualenvs
virtualenv ~/.virtualenvs/yola_auth_py3
source ~/.virtualenvs/yola_auth_py3/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata --app users users/fixtures/users.json
python manage.py runserver
```
## Registration
```bash
curl -H "Content-Type: application/json" -X POST -d '{"password":"$str0ng_p@$$w0rd", "email":"ikovalko@gmail.com"}' http://localhost:8000/api/v1/register/
```
## Login
```bash
key=$(curl -H "Content-Type: application/json" -X POST -d '{"password":"$str0ng_p@$$w0rd", "email":"ikovalko@gmail.com"}' http://localhost:8000/api/v1/login/ --cookie-jar cookie | cut -c9-48)
```

## Users API
### Using previously saved cookie
#### Users
```bash
curl --cookie cookie localhost:8000/api/v1/users/
```
#### User
```bash
curl --cookie cookie localhost:8000/api/v1/users/1/
```
#### Edit user
```bash
crsf=$(cat cookie | grep csrf | awk -F "\t" '{print $7}')
curl -H "Content-Type: application/json" -H "X-CSRFToken: $crsf" -X PATCH --cookie cookie -d '{"first_name":"Ivan"}' localhost:8000/api/v1/users/3/
```

### Using auth token
#### Users
```bash
curl -H "Authorization: Token $key" localhost:8000/api/v1/users/
```
#### User
```bash
curl -H "Authorization: Token $key" localhost:8000/api/v1/users/1/
```
#### Edit user
```bash
curl -H "Content-Type: application/json" -H "Authorization: Token $key" -X PATCH -d '{"first_name":"Ivan"}' localhost:8000/api/v1/users/3/
```
