import network
import time

from machine import Pin

def connect_to_wlan(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for WLAN connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('WLAN connection failed')
    
    status = wlan.ifconfig()
    ip = status[0]
    
    print(f'Connected to WLAN {ssid}. Assigned IP: {ip}')
    
    return ip