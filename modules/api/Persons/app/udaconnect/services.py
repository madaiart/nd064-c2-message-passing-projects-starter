import logging, json, grpc, time
from typing import Dict, List

from app import db

from app.udaconnect.models import Person

from modules.messages import connection_pb2, connection_pb2_grpc


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()


class ConnectionService:
    @staticmethod
    def find_contacts():
         # Cache all users in memory for quick lookup

            channel = grpc.insecure_channel("localhost:5001")
            stub = connection_pb2_grpc.ConnectionServiceStub(channel)
            response = stub.Get(connection_pb2.Empty())
            return response