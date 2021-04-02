FROM python:3.6.8
copy . /
WORKDIR /
RUN pip install -r requirements.txt



CMD ["python", "gui.py"]