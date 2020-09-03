# Investment Chatbot Investi

## Setup the project on your machine

### Prerequisites
* Python version >= 3.6

To check the Python version on your system, run
```bash
$ python --version
Python 3.6.8
```
or 
```bash
$ python3 --version
Python 3.6.8
```
If an older version than 3.6 or nothing is found you will need to [update or install Python](https://realpython.com/installing-python/) first. 

### Install the project on your machine

Clone the repository
```
$ git clone https://github.com/ottonieroeder/chatbot1.git
```

Setup a virtual env
 
```bash
$ python -m venv env
$ source env/bin/activate
```

Install requirements
```bash
$(env) cd chatbot1/
$(env) pip install -r requirements.txt
```

Download the English corpus
```bash
$(env) python -m spacy download en
```

Run migrations to setup the database 
```bash
$(env) python manage.py migrate
```

Run the development server
```bash
$(env) python manage.py runserver
```