FROM python:3.6.8
copy . /
WORKDIR /
RUN pip install -r requirements.txt
RUN add-apt-repository universe
RUN apt-get update
RUN apt-get install python3-pyqt5

CMD ["python", "gui.py"]
