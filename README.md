# UE WEB APP

Utilisation du framework Flask pour créer une application web de chat identique à What's App
<br/>
Ce Projet a été développé par Gabriela Bertoli et Eliot Boutet
    

### Extension:
- Restful: [Flask-restplus](http://flask-restplus.readthedocs.io/en/stable/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)


## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
|──────assets/
|──────database/
| |──────database.db
| |──────database.py
| |──────models.py
|──────node_modules/
|──────static/
| |──────js/
| |──────storage/
|──────templates/
| |────layouts/
| | |────layout.html.jinja2


```


## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```

## Lancer le serveur

Start server on port 5000 et en mode debug

```
FLASK_APP = app.py
FLASK_ENV = development
FLASK_DEBUG = 1
python -m flask run
```