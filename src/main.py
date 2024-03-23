from wlan_connection import connect_to_wlan
from http_server import HttpServer
import dht

from machine import Pin

def read_index(ip):
    file = open('index.html')
    content = file.read()
    
    file.close()
    
    updated_content = content.format(host_ip=ip)
    
    return updated_content

SSID = 'M-WiFi'
PASSWORD = "{t%GNuUK'BM;zFO"

ip = connect_to_wlan(SSID, PASSWORD)

http_server = HttpServer('0.0.0.0', 80, ip)

html = read_index(ip)

switch = {
    'led': Pin(15, Pin.OUT),
    'state': 0
}

sensor = dht.DHT11(Pin(14))

def handle_index(ctx):
    ctx.write_html(200, html)

def handle_all_devices(ctx):
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    
    data = {
        'temperature': temp,
        'humidity': hum,
        'switch': switch['state']
    }
    
    ctx.write_json(200, data)
    
def handle_hd11(ctx):
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    
    data = {
        'temperature': temp,
        'humidity': hum
    }
    
    ctx.write_json(200, data)
    
def handle_switch(ctx):
    data = {
        'message': 'success'        
    }
    
    if switch['state']:
        switch['state'] = 0
    else:
        switch['state'] = 1
        
    switch['led'].value(switch['state'])
    
    ctx.write_json(200, data)
    
http_server.register_route('/', 'GET', handle_index)
http_server.register_route('/api/all-devices', 'GET', handle_all_devices)
http_server.register_route('/api/hd11', 'GET', handle_hd11)
http_server.register_route('/api/switch', 'POST', handle_switch)

http_server.listen()