FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install .
RUN flask_backend create-db
RUN flask_backend populate-db
RUN flask_backend add-user -u admin -p admin
EXPOSE 5000
CMD ["flask_backend", "run"]
