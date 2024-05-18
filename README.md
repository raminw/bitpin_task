# Bitpin Task

## Development setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run database migrations
```bash
python manage.py migrate
```

### 3. Run server:

```bash
python manage.py runserver
```


### 4. Run Rating Process:
```bash
python manage.py process_rates
```


### 5. Cron Job Commands:
```bash
python manage.py crontab add
python manage.py crontab show
python manage.py crontab remove
```

## Documentation:
[implementation documents](https://docs.google.com/document/d/1I3YNbcMGZNwPNeuVBereZu-Um0WmBJ8mUiuZlhOBa8w/edit?usp=sharing) 


## API Documentation:
After running sever you can find API documentation in:
```
{Base_URL}/swagger/

{Base_URL}/docs/
```