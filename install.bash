python3 -m pip install virtualenv
mkdir -p ~/.virtualenvs
virtualenv ~/.virtualenvs/yola_auth_py3
source ~/.virtualenvs/yola_auth_py3/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata --app users users/fixtures/users.json
python manage.py runserver localhost:8000