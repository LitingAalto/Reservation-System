FROM python:3.6.8
copy . /
WORKDIR /

RUN sudo apt-get update 
RUN sudo apt-get install python3-pyqt5 -y
	  
RUN pip install -r requirements.txt

CMD ["python", "gui.py"]
