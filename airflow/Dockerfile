FROM apache/airflow:2.10.5

COPY requirements.txt .
USER root
RUN apt-get update && \
    apt-get install -y wget gnupg curl unzip && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb
USER airflow
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

