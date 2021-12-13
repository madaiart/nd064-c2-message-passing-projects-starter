import grpc

import coordinates_event_pb2
import coordinates_event_pb2_grpc

"""
Simulation from fake phone
"""

print("Phone sending...")

channel = grpc.insecure_channel("127.0.0.1:30001")
stub = coordinates_event_pb2_grpc.ItemServiceStub(channel)

# Update this with desired payload
user_coordinates = coordinates_event_pb2.EventCoordinatesMessage(
    userId=300,
    latitude=-100,
    longitude=30
)

user_coordinates_2 = coordinates_event_pb2.EventCoordinatesMessage(
    userId=400,
    latitude=-100,
    longitude=30
)

response_1 = stub.Create(user_coordinates)
response_2 = stub.Create(user_coordinates_2)


print("Coordinates sent...")
print(user_coordinates, user_coordinates_2)
