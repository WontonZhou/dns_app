import socket
import json

# define the port number and the file to store the DNS records
AS_PORT = 53533
DNS_RECORD_FILE = 'dns_records.json'


def load_dns_records():  # function to load DNS records
    with open(DNS_RECORD_FILE, 'r') as file:
        return json.load(file)


def save_dns_record(record):  # function to save DNS record
    records = load_dns_records()
    records[record["NAME"]] = record
    with open(DNS_RECORD_FILE, 'w') as file:
        json.dump(records, file, indent=4)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as AS:  # Create UDP socket
        AS.bind(('', AS_PORT))  # Bind to the port
        print(f"AS server running on port {AS_PORT}")  # Print the port number
        while True:
            data, addr = AS.recvfrom(2048)  # receive data from client including address
            data = json.loads(data.decode('utf-8'))  # decode the data into JSON
            if 'VALUE' in data:  # Registration request
                save_dns_record(data)
                response = {"ip": data['VALUE']}  # ip is needed here to work with US and FS
                response = json.dumps(response).encode('utf-8')
                print(f"Registered: {data}")
            else:  # Query request
                records = load_dns_records()
                response = json.dumps(records.get(data['NAME'], {"error": "500 Not Found"})).encode('utf-8')
                print(f"Queried: {data}")
            AS.sendto(response, addr)  # send the response to the client
