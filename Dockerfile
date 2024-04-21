FROM python:3.12-slim

COPY . /app
WORKDIR /app
RUN pip3 install -Ur requirements.txt

ENTRYPOINT [ "python3", "router.py" ]