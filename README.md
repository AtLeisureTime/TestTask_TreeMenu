# TestTask_TreeMenu
### Run locally
```
git clone https://github.com/AtLeisureTime/TestTask_TreeMenu.git
cd TestTask_TreeMenu/
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt

cd TreeMenu/
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data/menu_data.json
python manage.py runserver
```
