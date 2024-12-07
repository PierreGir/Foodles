## Setup Instructions :

1. Create a virtual environment and install dependencies
install the required dependencies using `pip`:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set Up the database
Run the following command to apply migrations and set up the database:
```
python manage.py migrate
python manage.py loaddata inventory/fixtures/initial_data.json
```

3. Run the server
After migrations are applied, you can start the server:
```
python manage.py runserver
```

4. Running Tests with pytest
To run the tests for the project, use `pytest`:
```
pytest