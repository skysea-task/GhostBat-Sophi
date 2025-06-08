FROM python:3.13

WORKDIR /root/RAUSHAN

COPY . .

# RUN apt-get update && apt-get install -y default-jre openjdk-17-jdk nodejs npm
RUN apt-get update && apt-get install ffmpeg -y
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -U -r requirements.txt

CMD ["python3", "-m", "RAUSHAN"]
