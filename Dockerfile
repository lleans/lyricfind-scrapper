FROM python:3.10-slim

COPY . /app
WORKDIR /app
RUN pip3 install -Ur requirements.txt

CMD ["python3", "router.py"]