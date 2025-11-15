FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app
RUN chmod +x start.sh
CMD ["./app/flights/start.sh"]