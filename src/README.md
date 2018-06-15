## API REST

### Clone the project

```git clone ```

#### Load dependencies

```pip install -r requirements.txt```

#### Run the project

You must be in the ```src``` directory

1. Create a Data Base and change in ```settings/settings.py```

2. ```./manage.py migrate```

2. ```./manage.py loaddata fixtures/initial.json```

3. ```./manage.py createsuperuser```

4. ```./manage.py runserver```