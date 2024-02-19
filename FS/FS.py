import json
import socket

from flask import Flask, request, jsonify

app = Flask(__name__)  # initialize Flask app
fib_cache = {}  # to avoid redundant calculations


@app.route('/register', methods=['PUT'])  # register the server to the AS
def register():
    data = request.json  # should be same as request.get_json() but with a different name
    hostname = data.get('hostname')
    FS_ip = request.args.get('ip')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, FS_ip, as_ip, as_port]):  # check if all parameters are present
        return jsonify({"error": "parameters missing"}), 400

    data = json.dumps({  # create the data to send to the AS
        "TYPE": "A",
        "NAME": hostname,
        "VALUE": FS_ip,
        "TTL": 10
    })

    as_port = int(as_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
    client.sendto(data.encode(), (as_ip, as_port))  # send the data to the AS
    message, addr = client.recvfrom(2048)  # receive the response from the AS
    response = message.decode()  # decode the response
    print(response)  # print the response
    if 'ip' in response and response['ip'] == FS_ip:  # check if the IP is registered
        return "Registration successful", 201
    else:
        return "Error", 500


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number', type=int)  # get the number from the request
    if number is None or type(number) is not int:
        return jsonify({"error": "not integer"}), 400  # return error if the number is not present or not an integer
    result = fib(number)
    return jsonify({"fibonacci number": result}), 200  # return the result


def fib(n):  # function to calculate Fibonacci number
    if n in fib_cache:
        return fib_cache[n]
    elif n <= 1:
        return n  # return 0 or 1
    else:
        fib_cache[n] = fib(n - 1) + fib(n - 2)  # calculate Fibonacci number and save it in cache
        return fib_cache[n]  # return the Fibonacci number


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=9090)
