# this is a script to test the AS server
# After testing all 4 requirements are furfilled:
# FS accepts a registration request in /register
# FS responds to GET requests in /fibonacci
# AS performs registration requests as specified
# AS provides DNS record for a given query

import socket
import json

AS_IP = '127.22.0.2'  # AS IP on my device
AS_PORT = 53533  # AS port

# test registration request
# the parameter can be changed to test different registration requests
def send_registration_request():
    registration_data = {  # as listed in the example
        "TYPE": "A",
        "NAME": "fibonacci.com",
        "VALUE": '172.22.0.4',
        "TTL": 10
    }
    message = json.dumps(registration_data)  # jsonize the data
    # send the message
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(message.encode(), (AS_IP, AS_PORT))
        response, _ = client_socket.recvfrom(2048)
        print("Registration Response:", response.decode())

# test DNS query
def send_dns_query():
    query_data = {
        "TYPE": "A",
        "NAME": "fibonacci.com"
    }
    message = json.dumps(query_data)
    # query the message, this should check the as server dns.txt and return the value
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(message.encode(), (AS_IP, AS_PORT))
        response, _ = client_socket.recvfrom(2048)
        print("DNS Query Response:", response.decode())


if __name__ == "__main__":
    print("Registration Request")
    send_registration_request()

    print("\nDNS Query")
    send_dns_query()
