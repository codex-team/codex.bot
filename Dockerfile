FROM python:3.9-slim-buster


WORKDIR /home/app

RUN pip install --upgrade pip
COPY ./requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]