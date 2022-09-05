FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apps ./apps
COPY ./core ./core
COPY ./media ./media
COPY ./staticfiles ./staticfiles
COPY ./manage.py .
COPY ./gunicorn-cfg.py .

# running migrations
RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
