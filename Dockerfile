FROM python:3.6.8
copy . /
WORKDIR /

RUN apt-get update \
 && apt-get install -y sudo

RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker

# this is where I was running into problems with the other approaches
RUN sudo apt-get update 
RUN sudo apt-get install python3-pyqt5 -y
	  
RUN pip install -r requirements.txt



#RUN add-apt-repository universe
#RUN apt-get update
#RUN apt-get install python3-pyqt5


CMD ["python", "gui.py"]
