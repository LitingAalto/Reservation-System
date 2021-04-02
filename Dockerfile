FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install python3-pip
RUN pip 3 install --upgrade pip
echo "something"