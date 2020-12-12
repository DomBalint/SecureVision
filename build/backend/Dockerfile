FROM python:3.7.2

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR .

COPY database/ ./backend/database
COPY api/ ./backend/api

CMD ["python", "backend/api/api_class.py"]
