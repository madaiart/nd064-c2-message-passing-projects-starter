FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers build-base

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .
ENTRYPOINT ["python", "grpc_server_startup.py"]