import os, json, logging, grpc

from concurrent import futures
from kafka import KafkaProducer

import coordinates_event_pb2
import coordinates_event_pb2_grpc

kafka_url = "kafka-release-0.kafka-release-headless.default.svc.cluster.local:9092"
kafka_topic = os.environ["KAFKA_TOPIC"]

logging.info('[Kafka] connecting...', kafka_url)
# print('connecting to kafka ', kafka_url)

logging.info('[Kafka] connecting topic... ', kafka_topic)
# print('connecting to kafka topic ', kafka_topic)

producer = KafkaProducer(bootstrap_servers=kafka_url)

class CoordinatesEventServicer(coordinates_event_pb2_grpc.ItemServiceServicer):

    def Create(self, request, context):
        request_value = {
            'userId': int(request.userId),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }

        logging.info('[Kafka] processing entity... ', request_value)

        user_encode_data = json.dumps(request_value, indent=2).encode('utf-8')
        producer.send(kafka_topic, user_encode_data)

        return coordinates_event_pb2.EventCoordinatesMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
coordinates_event_pb2_grpc.add_ItemServiceServicer_to_server(CoordinatesEventServicer(), server)

logging.info('[Kafka] starting on port 5001')
server.add_insecure_port('[::]:5001')
server.start()
server.wait_for_termination()
