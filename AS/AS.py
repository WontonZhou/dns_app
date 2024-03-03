# This is the AS server
from socket import *
import json
import os

server_port = 53533
as_socket = socket(AF_INET, SOCK_DGRAM)
as_socket.bind(('', server_port))

if not os.path.exists('dns.txt'):
    open('dns.txt', 'w').close()  # make sure dns.txt exists


def registration(request):
    with open('dns.txt', 'a', encoding='utf-8') as outfile:
        json.dump(request, outfile)
        outfile.write('\n')
    print('201 Registered')
    return '201 Registered'


def query(request):
    with open("dns.txt", 'r', encoding='utf-8') as infile:
        for line in infile:
            data = json.loads(line)
            if request['TYPE'] == data['TYPE'] and request['NAME'] == data['NAME']:
                print('200 OK')
                return json.dumps(data)
    print('404 Not Found')
    return '404 Not Found'


def process_request(request):
    if len(request) == 4:  # if there are 4 parameters, it is a registration request
        return registration(request)
    elif len(request) == 2:  # if there are 2 parameters, it is a query request
        return query(request)
    else:
        print('400 Bad Request')
        return '400 Bad Request'


while True:
    message, client_address = as_socket.recvfrom(2048)
    mes = json.loads(message.decode())
    response = process_request(mes)
    as_socket.sendto(response.encode(), client_address)

# def test_dns():
#     print("Current working directory:", os.getcwd())
#     registration_request = {
#         "TYPE": "A",
#         "NAME": "www.google.com",
#         "VALUE": "192.0.2.1",
#         "TTL": 10
#     }
#     print("registration request")
#     response = process_request(registration_request)
#     print(response)
#     query_request = {
#         "TYPE": "A",
#         "NAME": "example.com"
#     }
#     print("\nDNS query")
#     response = process_request(query_request)
#     print(response)
#
# test_dns()  # test the DNS server
