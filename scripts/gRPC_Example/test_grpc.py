import grpc

import coordinates_event_pb2
import coordinates_event_pb2_grpc


print("[gRPC] Coordinates sending...")

channel = grpc.insecure_channel("127.0.0.1:30001")
stub = coordinates_event_pb2_grpc.ItemServiceStub(channel)

# Update this with desired payload
user_coordinates = coordinates_event_pb2.EventCoordinatesMessage(
    userId=100,
    latitude=-87.4,
    longitude=0.2
)

user_coordinates_2 = coordinates_event_pb2.EventCoordinatesMessage(
    userId=110,
    latitude=-87.5,
    longitude=0.21
)

response_1 = stub.Create(user_coordinates)
response_2 = stub.Create(user_coordinates_2)


print("[gRPC] Coordinates sent...")
print(user_coordinates, user_coordinates_2)
