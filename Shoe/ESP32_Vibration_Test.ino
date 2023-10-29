#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include <WebServer.h>

const char* ssid = "worldhq";
const char* password = "iwillforeverbetheboss";   
const char* hostname = "esp32-left";

const int vibrate = 10;

WiFiServer server(80);

void setup()
{
    Serial.begin(115200);
    delay(10);
    WiFi.begin(ssid, password);
    MDNS.begin(hostname);
    server.begin();
    pinMode(vibrate, OUTPUT);
}

void loop()
{
    WiFiClient client = server.available();
    if (client) {
        String currentLine = "";
        while (client.connected()) {
            if (client.available()) {
                char c = client.read();
                if (c == '\n') {
                    if (currentLine.length() == 0) {
                        client.println("HTTP/1.1 200 OK");
                        client.println("Content-type:text/html");
                        client.println();
                        client.println("row and column received from esp32-left");
                        
                         // Read data from the request
                        String sensor_data;
                        while(client.available()){
                            String line = client.readStringUntil('\r');
                            if (line.startsWith("sensor_data=")) {
                                sensor_data = line.substring(12); // Assuming data starts after "sensor_data="
                                break;
                            }
                        }

                        // Split the string by '+'
                        int plusIndex = sensor_data.indexOf('+');
                        if (plusIndex != -1) {
                            String value1 = sensor_data.substring(0, plusIndex);
                            String value2 = sensor_data.substring(plusIndex + 1);

                            int intValue1 = value1.toInt();
                            int intValue2 = value2.toInt();

                            Serial.print("Row: ");
                            Serial.println(intValue1);
                            Serial.print("Column: ");
                            Serial.println(intValue2);

                            for (int i = 0; i < intValue1; i++) {
                              digitalWrite(vibrate, HIGH);
                              delay(250);
                              digitalWrite(vibrate, LOW);
                              delay(250);
                            }
                            delay(1000);
                            for (int i = 0; i < intValue2; i++) {
                              digitalWrite(vibrate, HIGH);
                              delay(250);
                              digitalWrite(vibrate, LOW);
                              delay(250);
                            }
                        }

                        break;
                    } else {
                        currentLine = "";
                    }
                } else if (c != '\r') {
                    currentLine += c;
                }
            }
        }
        client.stop();
    }
}