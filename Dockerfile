FROM python:3.11.8-slim-bullseye
# Add a work directory
WORKDIR /app
# Cache and Install dependencies
COPY requirements.txt /app/requirements.txt
RUN apt update
RUN apt-get install -y build-essential
RUN apt-get install -y python3-psycopg2
# RUN apt-get install -y python3-pip
RUN apt install -y python3-dev libpq-dev
RUN pip3 install -r /app/requirements.txt
COPY . /app
CMD ["python3", "main.py"]
