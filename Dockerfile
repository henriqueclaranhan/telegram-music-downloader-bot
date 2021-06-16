FROM debian:latest
	
RUN apt update && apt upgrade -y
RUN apt install git ffmpeg python3-pip -y
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN pip3 install -U -r requirements.txt
CMD python3 bot.py
