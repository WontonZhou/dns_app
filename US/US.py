# User server
from flask import Flask, request, jsonify
import requests
from socket import socket, AF_INET, SOCK_DGRAM
import json

app = Flask(__name__)  # initialize Flask app


@app.route('/fibonacci')  # route to get Fibonacci number
def fibonacci():
    # US contains 5 parameters: hostname, fs_port, number, as_ip, as_port
    hostname = request.args.get('hostname')  # hostname of server
    fs_port = request.args.get('fs_port')  # port num of server
    number = request.args.get('number')  # sequence numberX is the response for the Fibonacci num
    as_ip = request.args.get('as_ip')  # ip of AS
    as_port = request.args.get('as_port')  # port of AS

    # Check if the parameters are missing
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"error": "Missing parameters"}), 400  # return error message

    # Make sure they are integers
    fs_port = int(fs_port)
    number = int(number)
    as_port = int(as_port)

    fs_ip = query_dns(as_ip, int(as_port), hostname)  # get the IP of the FS server
    if not fs_ip:
        return jsonify({"error": "DNS query failed"}), 500  # return error message
    fib_response = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")  # get Fibonacci number
    if fib_response.status_code != 200:
        return jsonify({"error": "Error from Fibnacci Server"}), fib_response.status_code
    return fib_response.content, 200


def query_dns(as_ip, as_port, hostname):  # function to query DNS
    message = json.dumps({'TYPE': 'A', 'NAME': hostname})  # message to send
    with socket(AF_INET, SOCK_DGRAM) as s:  # create a socket
        s.sendto(message.encode(), (as_ip, as_port))  # send UDP message to AS server
        response, _ = s.recvfrom(2048)  # receive response and set the buffer zone to 2048
        info = json.loads(response.decode())  # decode the response into JSON
        return info.get('VALUE')  # return the value


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # run the app with port 8080
    #  host 0 0 0 0  is used to make the server publicly available
