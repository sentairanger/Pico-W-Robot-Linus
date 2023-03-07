# import libraries
import network
import socket
from time import sleep
from picozero import Robot, LED, Servo, PWMOutputDevice

# Define the pins
robot = Robot(left=(14, 15), right=(16, 17), pwm=False)
eye = LED(1, pwm=False)
servo_1 = Servo(18)
servo2 = Servo(19)
en_1 = PWMOutputDevice(20)
en_2 = PWMOutputDevice(21)

# Define the wifi network
ssid = 'yourssid'
password = 'yourpassword'

# Define connect function to connect to the network
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

# Define the open_socket function for the ip address
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

# Define the template
def webpage():
    #Template HTML
    with open("robot.html", 'r') as f:
        html = f.read()
    return html

# Serve the application here
def serve(connection):
    robot.stop()
    en_1.value = 0
    en_2.value = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        servo_response = request.find('servo=') + len('servo=')
        servo_response2 = request.find('servo2=') + len('servo2=')
        pwm = request.find('pwm=') + len('pwm=')
        if request[servo_response].isdigit():
            offset = 1
            if request[servo_response+1].isdigit():
                offset = 2
                if request[servo_response+2].isdigit():
                    offset = 3
            angle = int(request[servo_response:servo_response+offset])
            print(angle)
            servo_1.value = angle / 100
        if request[servo_response2].isdigit():
            offset = 1
            if request[servo_response2+1].isdigit():
                offset = 2
                if request[servo_response2+2].isdigit():
                    offset = 3
            angle2 = int(request[servo_response2:servo_response2+offset])
            print(angle2)
            servo2.value = angle2 / 100
        if request[pwm].isdigit():
            offset = 1
            if request[pwm+1].isdigit():
                offset = 2
                if request[pwm+2].isdigit():
                    offset = 3
            speed = int(request[pwm:pwm+offset])
            print(speed)
            en_1.value = speed / 10
            en_2.value = speed / 10
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
        if request == "/on?":
            eye.on()
        if request == "/off?":
            eye.off()
        html = webpage()
        try:
            html = html.replace('slider_value', str(value))
            html = html.replace('slider_value2', str(value))
            html = html.replace('slider_value3', str(value))
        except Exception as e:
            html = html.replace('slider_value', '0')
            html = html.replace('slider_value2', '0')
            html = html.replace('slider_value3', '0')
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
