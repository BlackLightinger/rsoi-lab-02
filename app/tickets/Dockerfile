FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/tickets/ ./
COPY common.py ./
COPY services.py ./

RUN chmod +x start.sh

CMD [".start.sh"]