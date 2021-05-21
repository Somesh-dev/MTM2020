
# importing the requests library 
import requests
import time
import lcddriver
  

counter_id=23 #change counter_id to fetch the data from different counter
URL= "http://192.86.32.153:5000/getcounter/"+str(counter_id)

# Load the driver and set it to "display"
display = lcddriver.lcd()

# extracting data in json format
n2=""
while True:
    r = requests.get(url = URL) 
    data = r.json()
    n1 = data["name"]
    p1 = data["pack"]
    ph1 = data["phone"]
    if (n1 != n2):
        n2=n1
        print ("Name: " + n1)
        if (p1=="CP"):
            p1="Custom"
        else:
            p1 = "$"+p1
        print ("Price: " + p1)
        print("Phone: "+ ph1)
        display.lcd_display_string("Name: loading", 1)
        display.lcd_display_string("Price: loading", 2)
        time.sleep(2)
        display.lcd_clear()
        display.lcd_display_string(n1, 1)
        display.lcd_display_string("Payment: "+p1, 2)
        time.sleep(5)