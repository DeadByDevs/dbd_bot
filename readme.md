#deadbybot

## required library:

python-dotenv
discord.py
requests
pillow
numpy

## how to set up the environment :

- create bot-env

  - python3 -m venv bot-env

- activate virtual env:

  - source bot-env/bin/activate

- install in env

  - pip install -U discord.py

- add packages to requirements.txt

  - pip freeze > requirements.txt

- install requirements

  - pip install -r requirements.txt

## how to run the bot :

- activate virtual env if not already in it:
  - source bot-env/bin/activate
- run bot:
  - python3 main.py
