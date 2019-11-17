#include <WiFi.h>
#include <ESP32Servo.h>

Servo myservo;

//const char* ssid = "elecom2g-c08850"; //サーバーのSSID
//const char* password = "3A7344CE7169FD2122B9F397AA3EB79F212E5E0741AEF3BB5A5E6BC652F15C0F"; //サーバーのパスワード
const char* ssid = "ist_members"; //サーバーのSSID
const char* password = "8gAp3nY!s2Gm"; //サーバーのパスワード

//const char* host = "192.168.2.110";
const char* host = "157.82.207.143";


void setup() {
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }
  WiFi.config(IPAddress(157, 82, 207, 141), WiFi.gatewayIP(), WiFi.subnetMask());
  //  WiFi.config(IPAddress(192, 168, 2, 107), WiFi.gatewayIP(), WiFi.subnetMask());
  Serial.println(WiFi.localIP());

  myservo.attach(14);
  postToServer("set_moving", "0");
}

void loop() {
  // 巻き取るか確認
  int goHome = postToServer("get_goHome", "").toInt();
  // 0なら停止のまま
  if (goHome == 0) {
    postToServer("set_moving", "0");
    delay(1000);
  }
  // 1なら巻き取る
  else if (goHome == 1) {
    postToServer("set_moving", "1");
    myservo.write(90 + 90);
    while (goHome == 1) {
      goHome = postToServer("get_goHome", "").toInt();
      delay(1000);
      postToServer("set_moving", "0");
    }
    myservo.write(90);
    postToServer("set_moving", "0");
  }
  // -1なら弛ませる
  else if (goHome == -1) {
    postToServer("set_moving", "-1");
    myservo.write(90 - 8);
    while (goHome == -1) {
      goHome = postToServer("get_goHome", "").toInt();
      delay(1000);
      postToServer("set_moving", "0");
    }
    myservo.write(90);
    postToServer("set_moving", "0");
  }
  //}
  //myservo.write(90 + 90);
  //delay(18000);
  //myservo.write(90 - 8);
  //delay(30000);
}

//POST
String postToServer(String Name, String Data) {
  Serial.print("connecting to ");
  Serial.println(host);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    ESP.restart();
    //    esp_wifi_restore();
    return "connection failed";
  }

  // We now create a URI for the request
  // This will send the request to the server
  const String bodyJ = "{\"Name\":\"" + Name + "\",\"Data\":\"" + Data + "\"}";
  const String str = String("POST") + " http://" + host + " HTTP/1.1\r\n" +
                     "Host: " + "80" + "\r\n" +
                     "Content-Length: " + String(bodyJ.length()) + "\r\n" +
                     "Content-Type: application/json\r\n" +
                     "Connection: close\r\n\r\n";
  const String request = str + bodyJ;
  client.print(request);
  //  Serial.println(request);
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 5000) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return "Client Timeout";
    }
  }

  // Read all the lines of the reply from server and print them to Serial
  String response = "";
  while (client.available()) {
    response = client.readStringUntil('\r');
    //    Serial.print(line);
  }

  Serial.println(response);
  Serial.println("closing connection");
  return response;
}

void moveServo() {
  myservo.write(90 - 90);
  delay(4000);
  myservo.write(90);
}
