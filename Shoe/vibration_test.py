import requests

esp32_hostname = "esp32-left.local"  # Replace with your actual mDNS hostname
url = f"http://{esp32_hostname}/endpoint"  # Define the URL of your ESP32 endpoint

data = {'sensor_data': '69696969'}  # Replace with your actual data

response = requests.post(url, data=data)

print(response.text)
