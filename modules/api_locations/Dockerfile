FROM python:3.7-alpine

WORKDIR .

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .
ENTRYPOINT ["python", "grpc_server_startup.py"]