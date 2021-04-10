FROM python:3.9.4-alpine
EXPOSE 8080

WORKDIR /flask

COPY requirements.txt /flask
RUN pip install -r requirements.txt

COPY . /flask/
CMD python app.py
