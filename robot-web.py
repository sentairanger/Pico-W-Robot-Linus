import network
import socket
from time import sleep
from picozero import Robot

robot = Robot(left=(14, 15), right=(16, 17))

ssid = ''
password = ''

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    #Template HTML
    with open("robot.html", 'r') as f:
        html = f.read()
    return html

def serve(connection):
    robot.stop()
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == "/forward?":
            robot.forward()
        if request == "/backward?":
            robot.backward()
        if request == "/left?":
            robot.left()
        if request == "/right?":
            robot.right()
        if request == "/stop?":
            robot.stop()
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
