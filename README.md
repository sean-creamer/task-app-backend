# Backend

This repo contains the server and the database code for the Task App. 

Note that this was done in a very limited amount of time and is in the 
same state as after the interview, as requested by Craig. Don't judge too harsh!

## Prerequisites 

### Create a virtual environment 

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Create & seed the database

Run the following command from the root level of the directory.

Also ensure you have `sqlite3` installed
```bash
make db
```

You can find the login information for the seeded users
in the `sql/users/seed_users_table.py` script.

### Create a .env file

Create a .env file in the root level of the repo with the 
following variables:

```
OPENAI_API_KEY = <I will provide my API key by email>
SECRET_KEY = <Use below command>
```

To generate the secret key, you can do something like:

```
openssl rand -base64 32
```

### Run the server 

```bash
uvicorn main:app --reload
```