# Ai News Update

## Development

### Installation

- Copy the `.env.dev` file to `.env` and configure the necessary fields.
- Run the following command to build and start the Docker containers:

```python
docker-compose up --build
```

Make sure to run the collectstatic, and migrate commands after this step.

Update readme 

### Some useful command

- Create a superuser

```
python manage.py createsuperuser
```

- Crawl the news from the future.io

```
python manage.py crawl
```

- Summary the latest news

```
python manage.py summary
```

- Send the latest news to the Slack channel

```
python manage.py slack_notice
```
