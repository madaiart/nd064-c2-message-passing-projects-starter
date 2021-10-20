import grpc, time
from typing import List
from app import db

from app.udaconnect.models import  Person

from modules.messages import person_pb2, person_pb2_grpc
from concurrent import futures


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    @staticmethod
    def retrieve_all(self, request, context) -> List[Person]:
        result = person_pb2.PersonList()
        result.persons.extend(db.session.query(Person).all())
        return result

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)

print("grpc Server starting on port 5002...")
server.add_insecure_port("[::]:5002")
server.start()

# Keep thread alive
try:
    while True: 
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
    