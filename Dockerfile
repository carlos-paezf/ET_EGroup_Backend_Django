FROM python:3.11.2

RUN apt-get update 

RUN apt install libpq-dev

# RUN apt install python-dev

WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/
# COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code/
# COPY . .

EXPOSE 8000

# RUN python manage.py seed core --number=100

CMD [ "python",  "manage.py", "runserver", "--noreload" ]