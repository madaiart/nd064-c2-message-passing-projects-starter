import logging, json, grpc, time
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from kafka import KafkaConsumer

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

from modules.messages import connection_pb2, connection_pb2_grpc, person_pb2, person_pb2_grpc
from concurrent import futures

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

TOPIC_NAME = 'conections'


class ConnectionServicer(connection_pb2_grpc.ConnectionServiceServicer):
    @staticmethod
    def find_contacts() -> List[Connection]:
        
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """

        consumer = KafkaConsumer(TOPIC_NAME)
        for msg in consumer:

            out = json.loads(msg)

            locations: List = db.session.query(Location).filter(
                Location.person_id == out["person_id"]
            ).filter(Location.creation_time < out["end_date"]).filter(
                Location.creation_time >= out["start_date"]
            ).all()

            # Cache all users in memory for quick lookup

            channel = grpc.insecure_channel("localhost:5002")
            stub = person_pb2_grpc.PersonServiceStub(channel)
            response = stub.Get(person_pb2.Empty())
            
            person_map: Dict[str, Person] = {person.id: person for person in response}

            # Prepare arguments for queries
            data = []
            for location in locations:
                data.append(
                    {
                        "person_id": out["person_id"],
                        "longitude": location.longitude,
                        "latitude": location.latitude,
                        "meters": out["meters"],
                        "start_date": out["start_date"].strftime("%Y-%m-%d"),
                        "end_date": (out["end_date"] + timedelta(days=1)).strftime("%Y-%m-%d"),
                    }
                )

            query = text(
                """
            SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
            FROM    location
            WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
            AND     person_id != :person_id
            AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
            AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
            """
            )
            result: List[Connection] = []
            for line in tuple(data):
                for (
                    exposed_person_id,
                    location_id,
                    exposed_lat,
                    exposed_long,
                    exposed_time,
                ) in db.engine.execute(query, **line):
                    location = Location(
                        id=location_id,
                        person_id=exposed_person_id,
                        creation_time=exposed_time,
                    )
                    location.set_wkt_with_coords(exposed_lat, exposed_long)

                    result.append(
                        Connection(
                            person=person_map[exposed_person_id], location=location,
                        )
                    )
        result_grpc = connection_pb2.ConnectionsList()
        result_grpc.connection.extend(result)
        return result_grpc

# Initialize gRPC Server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)

print("grpc Server starting on port 5001...")
server.add_insecure_port("[::]:5001")
server.start()

# Keep thread alive
try:
    while True: 
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)