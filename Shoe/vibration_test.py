import requests

esp32_hostname = "esp32-left.local"  # Replace with your actual mDNS hostname
url = f"http://{esp32_hostname}/endpoint"  # Define the URL of your ESP32 endpoint

while True:
    row = input("Enter row: ")
    if row.lower() == 'exit':
        break
    # row_data = {'sensor_data': row}
    col = input("Enter column: ")
    if col.lower() == 'exit':
        break
    # col_data = {'sensor_data': col}
    row_col = f'{row} {col}'
    send_data = {'sensor_data': row_col}
    response = requests.post(url, data=send_data)
    # response = requests.post(url, data=row_data)
    # response = requests.post(url, data=col_data)

    print(response.text)
