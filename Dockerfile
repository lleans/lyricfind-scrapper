FROM python:3.12-slim

COPY . /app
WORKDIR /app
RUN pip3 install -Ur requirements.txt

CMD python3, router.py