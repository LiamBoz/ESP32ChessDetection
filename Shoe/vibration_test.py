import requests

esp32_hostname = "esp32-shoe.local"  # Replace with your actual mDNS hostname
url = f"http://{esp32_hostname}/endpoint"  # Define the URL of your ESP32 endpoint

while True:
    piece = input("Enter piece number: ")
    if piece.lower() == 'exit':
        break
    row = input("Enter row: ")
    if row.lower() == 'exit':
        break
    # row_data = {'sensor_data': row}
    col = input("Enter column: ")
    if col.lower() == 'exit':
        break
    # col_data = {'sensor_data': col}
    piece_row_col = f'{piece} {row} {col}'
    send_data = {'sensor_data': piece_row_col}
    response = requests.post(url, data=send_data)
    # response = requests.post(url, data=row_data)
    # response = requests.post(url, data=col_data)
    
    print(response.text)
