#include <WiFi.h>
#include <WiFiUdp.h>
#include <ESP32Servo.h>

#define N 1024

const char* ssid = "elecom2g-c08850"; //サーバーのSSID
const char* password = "3A7344CE7169FD2122B9F397AA3EB79F212E5E0741AEF3BB5A5E6BC652F15C0F"; //サーバーのパスワード
const int port = 8000;
int goHome = 0;

// The udp library class
WiFiUDP udp;

Servo myservo;

void setup_wifi() {
  // setup wifi
  WiFi.mode(WIFI_STA);  // WIFI_AP, WIFI_STA, WIFI_AP_STA or WIFI_OFF
  WiFi.begin(ssid, password);
  // Connecting ..
  while (WiFi.status() != WL_CONNECTED) {

    Serial.println("Connection Failed! Rebooting...");
    delay(100);
  }
    WiFi.config(IPAddress(192, 168, 2, 102), WiFi.gatewayIP(), WiFi.subnetMask());
  Serial.println(WiFi.localIP());
  udp.begin(port);
}

void setup() {
    Serial.begin(115200);
  setup_wifi();
  myservo.attach(14);
}

void loop() {
  char packetBuffer[N];
  int packetSize = udp.parsePacket();

  // get packet
  if (packetSize) {
    int len = udp.read(packetBuffer, packetSize);
    if (len > 0) {
      packetBuffer[len] = '\0'; // end
    }
    goHome = atoi(packetBuffer);
    // print param
    Serial.println(goHome);
  }
  if (goHome == 1) {
    myservo.write(90 + 90);
  }
  else if (goHome == -1) {
    myservo.write(90 - 90);
  }
  else if (goHome == 0) {
    myservo.write(90);
  }
}

