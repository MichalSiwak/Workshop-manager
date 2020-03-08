FROM python:3.6.9
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
WORKDIR /app
COPY . .
EXPOSE 8000
CMD python manage.py runserver