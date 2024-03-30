FROM python:3.10

WORKDIR /app

COPY main.py /app/main.py
COPY constants.py /app/constants.py
COPY .env /app/.env
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]