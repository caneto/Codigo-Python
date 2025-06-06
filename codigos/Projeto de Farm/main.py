from machine import Pin, SoftI2C
from machine import Pin, ADC
from i2c_lcd import I2cLcd
import network
import time
import socket
import _thread
import dht

# FAN
fan = Pin(32, Pin.OUT)
fan.off()

# PUMP
pump = Pin(33, Pin.OUT)
pump.off()

# LCD
i2c = SoftI2C(scl=Pin(22), sda=Pin(21),freq=100000)
lcd = I2cLcd(i2c, 0x27,2,16)
time.sleep(1)
lcd.clear()

# DHT11
d = dht.DHT11(Pin(23))
t = 0
h = 0

def check_temp():
    print('Check Temp Starting...')
    global t
    global h
    while True:
        try:
            d.measure()
            time.sleep(2)
            t = d.temperature()
            h = d.humidity()
            temp = 'Temp: {:.0f} C'.format(t)
            humid = 'Humidity: {:.0f} %'.format(h)
            print('DHT11:', t, h)
            time.sleep(5)
        except:
            pass

# Soil Moisture
soil = ADC(Pin(35))
m = 100

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095

def check_moisture():
    print('Check Moisture Starting...')
    global m
    while True:
        try:
            soil.read()
            time.sleep(2)
            m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
            moisture = 'Soil Moisture: {:.1f} %'.format(m)
            print("Soil Moisture: " + "%.1f" % m +"% (adc: "+str(soil.read())+")")
            time.sleep(5)
        except:
            pass

# START
text = 'Starting...'
lcd.putstr(text)

# WIFI
wifi = 'Your_ssid' # your wifi ssid
password = 'Your_Password' # your wifi password
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
time.sleep(3)
wlan.connect(wifi, password)
time.sleep(5)
status = wlan.isconnected() # True/False
ip ,_ ,_ ,_ = wlan.ifconfig()

if status == True:
    lcd.clear()
    text = 'IP:{}'.format(ip)
    lcd.putstr(text)
    time.sleep(2)
    lcd.clear()
    lcd.putstr('Connected')
else:
    lcd.clear()
    lcd.putstr('Disconnected')

# HTML
html_fan_on = '''
<!doctype html>
<html lang="en">
  <body>
  <div class="container">
  <form>
    <center>
      <table>
      <tr>
      <th><h2 style="background-color:#ffa500; font-family:verdana;">FAN: ON</h2>
        <button  class="button button1" name="FAN" value="ON" type="submit">ON</button>
        <button  class="button button2" name="FAN" value="OFF" type="submit">OFF</button>
        <button  class="button button3" name="FAN" value="AUTO" type="submit">AUTO</button></th>
      </tr>
      </table><br>
    </center>
   </form>
  </div>
  </body>
</html>
'''

html_fan_off = '''
<!doctype html>
<html lang="en">
  <body>
  <div class="container">
  <form>
    <center>
      <table>
      <tr>
      <th><h2 style="background-color:#e7e7e7; font-family:verdana;">FAN: OFF</h2>
        <button  class="button button1" name="FAN" value="ON" type="submit">ON</button>
        <button  class="button button2" name="FAN" value="OFF" type="submit">OFF</button>
        <button  class="button button3" name="FAN" value="AUTO" type="submit">AUTO</button></th>
      </tr>
      </table><br>
    </center>
   </form>
  </div>
  </body>
</html>
'''

html_fan_auto = '''
<!doctype html>
<html lang="en">
  <body>
  <div class="container">
  <form>
    <center>
      <table>
      <tr>
      <th><h2 style="background-color:#ffa500; font-family:verdana;">FAN: AUTO</h2>
        <button  class="button button1" name="FAN" value="ON" type="submit">ON</button>
        <button  class="button button2" name="FAN" value="OFF" type="submit">OFF</button>
        <button  class="button button3" name="FAN" value="AUTO" type="submit">AUTO</button></th>
      </tr>
      </table><br>
    </center>
   </form>
  </div>
  </body>
</html>
'''

html_pump_on = '''
<!doctype html>
<html lang="en">
  <body>
  <div class="container">
  <form>
    <center>
      <table>
      <tr>
      <th><h2 style="background-color:#ffa500; font-family:verdana;">PUMP: ON</h2>
        <button  class="button button1" name="PUMP" value="ON" type="submit">ON</button>
        <button  class="button button2" name="PUMP" value="OFF" type="submit">OFF</button>
        <button  class="button button3" name="PUMP" value="AUTO" type="submit">AUTO</button></th>
      </tr>
      </table><br>
    </center>
   </form>
  </div>
  </body>
</html>
'''

html_pump_off = '''
<!doctype html>
<html lang="en">
  <body>
  <div class="container">
  <form>
    <center>
      <table>
      <tr>
      <th><h2 style="background-color:#e7e7e7; font-family:verdana;">PUMP: OFF</h2>
        <button  class="button button1" name="PUMP" value="ON" type="submit">ON</button>
        <button  class="button button2" name="PUMP" value="OFF" type="submit">OFF</button>
        <button  class="button button3" name="PUMP" value="AUTO" type="submit">AUTO</button></th>
      </tr>
      </table><br>
    </center>
   </form>
  </div>
  </body>
</html>
'''

html_pump_auto = '''
<!doctype html>
<html lang="en">
  <body>
  <div class="container">
  <form>
    <center>
      <table>
      <tr>
      <th><h2 style="background-color:#ffa500; font-family:verdana;">PUMP: AUTO</h2>
        <button  class="button button1" name="PUMP" value="ON" type="submit">ON</button>
        <button  class="button button2" name="PUMP" value="OFF" type="submit">OFF</button>
        <button  class="button button3" name="PUMP" value="AUTO" type="submit">AUTO</button></th>
      </tr>
      </table><br>
    </center>
   </form>
  </div>
  </body>
</html>
'''

html1 = '''
<!doctype html>
<html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <title>ESP32 - Status</title>
    <style>
    .button {
      border: none;
      border-radius: 4px;
      color: white;
      padding: 7px 12px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      margin: 1px 1px;
      cursor: pointer;
    }
    .button1 {background-color: #0d6efd;} /* Blue */
    .button2 {background-color: #dc3545;} /* Red */
    .button3 {background-color: #198754;} /* Green */
    </style>
  </head>
  <body style="font-family:verdana;">
  <div class="container">
  <form>
    <center>
    <h2><b>ESP32 Mini Smart Farm<b></h2>
    <h2>
'''

html2 = '''
    </h2><br>
    </center>
    </form>
  </div>
  </body>
</html>
'''

html_br = '''
     <br>
'''

# RUN
global fan_status
global pump_status
fan_status = 'OFF'
pump_status = 'OFF'

def runserver():
    global fan_status
    global pump_status
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    port = 80
    s.bind((host,port))
    s.listen(5)

    while True:
        client, addr = s.accept()
        print('Connection from: ', addr)
        data = client.recv(1024).decode('utf-8')
        print([data])
        
        try:
            check = data.split()[1].replace('/','').replace('?','')
            print('CHECK:',check)
            temp = 'Temp: {:.0f} C'.format(t)
            humid = 'Humidity: {:.0f} %'.format(h)
            moisture = 'Soil Moisture: {:.1f} %'.format(m)
                    
            if check != '':
                device_name, device_value = check.split('=')
                if device_name == 'FAN' and device_value == 'ON':
                    fan.on()
                    fan_status = 'ON'
                elif device_name == 'FAN' and device_value == 'OFF':
                    fan.off()
                    fan_status = 'OFF'
                elif device_name == 'FAN' and device_value == 'AUTO':
                    fan_status = 'AUTO'
                elif device_name == 'PUMP' and device_value == 'ON':
                    pump.on()
                    pump_status = 'ON'
                elif device_name == 'PUMP' and device_value == 'OFF':
                    pump.off()
                    pump_status = 'OFF'
                elif device_name == 'PUMP' and device_value == 'AUTO':
                    pump_status = 'AUTO'
            else:
                pass

            if fan_status == 'OFF' and pump_status == 'OFF':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_off + html_pump_off)
                client.close()
            elif fan_status == 'ON' and pump_status == 'OFF':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_on + html_pump_off)
                client.close()
            elif fan_status == 'OFF' and pump_status == 'ON':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_off + html_pump_on)
                client.close()
            elif fan_status == 'ON' and pump_status == 'ON':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_on + html_pump_on)
                client.close()
            elif fan_status == 'AUTO' and pump_status == 'OFF':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_auto + html_pump_off)
                client.close()
            elif fan_status == 'AUTO' and pump_status == 'ON':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_auto + html_pump_on)
                client.close()
            elif fan_status == 'OFF' and pump_status == 'AUTO':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_off + html_pump_auto)
                client.close()
            elif fan_status == 'ON' and pump_status == 'AUTO':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_on + html_pump_auto)
                client.close()
            elif fan_status == 'AUTO' and pump_status == 'AUTO':
                client.send(html1 + temp + html_br + humid + html_br + moisture + html2 + html_fan_auto + html_pump_auto)
                client.close()
            else:
                pass

            global fan_status
            global pump_status

        except:
            pass

def show_lcd():
    while True:
        try:
            temp = 'Temp: {:.0f} C'.format(t)
            humid = 'Humidity: {:.0f} %'.format(h)
            moisture = 'Moisture: {:.1f} %'.format(m)
            fan_s = 'FAN : {:}'.format(fan_status)
            pump_s = 'PUMP: {:}'.format(pump_status)
            lcd.clear()
            lcd.putstr(fan_s)
            lcd.move_to(0,1)
            lcd.putstr(pump_s)
            time.sleep(2)
            lcd.clear()
            lcd.putstr(temp)
            lcd.move_to(0,1)
            lcd.putstr(humid)
            time.sleep(2)
            lcd.clear()
            lcd.putstr(moisture)
            time.sleep(2)
        except:
            pass

def auto_pump():
    global pump_status
    while True:
        if m < 20 and pump_status == 'AUTO':
            time.sleep(1)
            pump.on()
            pump_status = 'ON (AUTO)'
            time.sleep(5)    # TURN ON PUMP 5 sec
            pump.off()
            pump_status = 'OFF (AUTO)'
            pump_status = 'AUTO'
            time.sleep(10)
        else:
            pass

def auto_fan():
    global fan_status
    while True:
        if t > 30 and fan_status == 'AUTO':
            time.sleep(1)
            fan.on()
            fan_status = 'ON (AUTO)'
            time.sleep(10)    # TURN ON FAN 10 sec
            fan.off()
            fan_status = 'OFF (AUTO)'
            fan_status = 'AUTO'
            time.sleep(10)
        else:
            pass

_thread.start_new_thread(runserver,())
_thread.start_new_thread(check_temp,())
_thread.start_new_thread(check_moisture,())
_thread.start_new_thread(show_lcd,())
_thread.start_new_thread(auto_pump,())
_thread.start_new_thread(auto_fan,())