Re:actor
===

## How to install

#### Repository Setting
- Clone git repository.
- `$ virtualenv .packages`
- `$ source .packages/bin/activate`
- `$ pip install -r requirements.txt`
- `$ mkdir config`
- `$ touch config/env.py`
- `$ echo "ENV = 'dev'" >> config/env.py`

#### Packages

##### Mac

- `$ brew install gettext`
- `$ brew link gettext --force`

## How to run

- `$ sh dev all`
- Access to `http://localhost:8000`.

## How to end

- `$ sh dev kill`
