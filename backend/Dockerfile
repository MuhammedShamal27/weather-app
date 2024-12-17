FROM python:3.14-rc-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
COPY certs/ /app/certs/


EXPOSE 5000

CMD ["python", "app.py"]
