#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include <WebServer.h>

const char* ssid = "worldhq";
const char* password = "iwillforeverbetheboss";   
const char* hostname = "esp32-left";

WiFiServer server(80);

void setup()
{
    Serial.begin(115200);
    delay(10);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    MDNS.begin(hostname);

    server.begin();
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
                        client.println("Hello from ESP32!");
                        
                        // Read data from the request
                        while(client.available()){
                            String line = client.readStringUntil('\r');
                            if (line.startsWith("sensor_data=")) {
                                Serial.println(line.substring(12)); // Assuming data starts after "sensor_data="
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