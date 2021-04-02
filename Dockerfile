FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

copy . /
WORKDIR /

CMD ["gui.py"]