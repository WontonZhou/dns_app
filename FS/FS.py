import json
import socket

from flask import Flask, request, jsonify

fib_cache = {}  # to avoid redundant calculations

app = Flask(__name__)


@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    hostname = data.get('hostname')
    FS_ip = request.host  # get the IP of the FS server
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, FS_ip, as_ip, as_port]):
        return "error 400"

    # Send the registration request to AS
    register_data = json.dumps({
        "TYPE": "A",
        "NAME": hostname,
        "VALUE": FS_ip,
        "TTL": 10
    })

    as_port = int(as_port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.sendto(register_data.encode(), (as_ip, as_port))
        message, _ = client.recvfrom(2048)
        response = message.decode()

    # error handling
    try:
        response_data = json.loads(response)
        if 'status' in response_data and response_data['status'] == 'success':
            return "Registration Successful 201"
        else:
            return "error 500"
    except json.JSONDecodeError:
        return "error 500"


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number', type=int)  # get the number from the request
    if number is None or type(number) is not int:
        return "error 400"  # return error if the number is not present or not an integer
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
