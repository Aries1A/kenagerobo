#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <ESP32Servo.h>

Servo myservo1, myservo2, myservo3; // 右前, 後ろ, 左前

//const char* ssid = "elecom2g-c08850"; //サーバーのSSID
//const char* password = "3A7344CE7169FD2122B9F397AA3EB79F212E5E0741AEF3BB5A5E6BC652F15C0F"; //サーバーのパスワード
const char* ssid = "ist_members"; //サーバーのSSID
const char* password = "8gAp3nY!s2Gm"; //サーバーのパスワード
//const char* ssid="Prototyping & Design Lab. 5GHz"; //サーバーのSSID
//const char* pass=""; //サーバーのパスワード


const char* host = "192.168.2.110";
//const char* host = "157.82.207.143";

const int IND_NUM = 10;
const int EXECUTE_NUM = 3;

int state, ind_count;
String indivisuals;
String servoInds[IND_NUM] = {"\0"};


void setup() {
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }
//  WiFi.config(IPAddress(157, 82, 207, 143), WiFi.gatewayIP(), WiFi.subnetMask());
  WiFi.config(IPAddress(192, 168, 2, 107), WiFi.gatewayIP(), WiFi.subnetMask());
  Serial.println(WiFi.localIP());


  //WiFi経由で書き込むためのもの
  ArduinoOTA
  .onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH)
      type = "sketch";
    else // U_SPIFFS
      type = "filesystem";

    // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
    Serial.println("Start updating " + type);
  })
  .onEnd([]() {
    Serial.println("\nEnd");
  })
  .onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  })
  .onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });

  ArduinoOTA.begin();

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  state = 0;
  myservo1.attach(2);
  myservo2.attach(4);
  myservo3.attach(18);
}

//実行
void execute(int state) {

  if (state == 0) {
    //遺伝子待機
    delay(5000);
  }
  else if (state == 1) {
    //動作
    moveServo(servoInds[ind_count]);
  }
  else if (state == 2) {
    //測位待機
    Serial.println(postToServer("calc_fit_val"));
  }
  else if (state == 3) {
    //遺伝子の更新待機
    delay(100);
  }
  else if (state == 4) {
    //学習終了状態

  }
  setNextState(state);
}

//状態更新
void setNextState(int currentstate) {
  if (currentstate == 0) {
    indivisuals = postToServer("get_indivisuals");
    //    Serial.println(indivisuals);
    //遺伝子取得成功
    if (indivisuals.length() > 2) {
      decode_indivisuals(indivisuals);
      Serial.println("Servo Start");
      state = 1;
      ind_count = 0;
    }
    //遺伝子が空（初回のみ）
    else {
      Serial.println("No indivisuals");
      state = 0;
    }
  }
  else if (currentstate == 1) {
    //動作終了
    ind_count++;
    state = 2;
  }
  else if (currentstate == 2) {
    //全ての個体の動作完了
    if (ind_count >= IND_NUM) {
      state = 3;
    }
    //未完了
    else {
      state = 1;
    }
  }
  else if (currentstate == 3) {
    //遺伝子の更新完了
    if (postToServer("get_evalready").toInt() == 0) {
      state = 0;
    }
    //未完了
    else {
      delay(1000);
      state = 3;
    }
    //学習完了
    if (postToServer("get_isStop").toInt() == 1) {
      state = 4;
    }

  }
  else if (currentstate == 4) {
    //学習終了状態
    if (ind_count >= IND_NUM) {
      ind_count == 0;
    }
    state = 0;
  }
}

//indivisualsのデコード
void decode_indivisuals(String indivisuals) {
  for (int i = 0; i < IND_NUM; i++) {
    servoInds[i] = {"\0"};
  }
  split(indivisuals, ',', servoInds);
  Serial.println("Got Ind: " + servoInds[0]);
}

void loop() {
  ArduinoOTA.handle();
  Serial.println("Current State is " + String(state));
  execute(state);
  //  const String response = postToServer("{\"Name\":\"get_indivisuals\"}");
  //  Serial.println(response);
}

//ここから便利ツール的関数
//split関数
int split(String data, char delimiter, String *dst) {
  int index = 0;
  int arraySize = (sizeof(data) / sizeof((data)[0]));
  int datalength = data.length();
  for (int i = 0; i < datalength; i++) {
    char tmp = data.charAt(i);
    if ( tmp == delimiter ) {
      index++;
      if ( index > (arraySize - 1)) return -1;
    }
    else dst[index] += tmp;
  }
  return (index + 1);
}

//POST
String postToServer(String body) {
  Serial.print("connecting to ");
  Serial.println(host);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return "connection failed";
  }

  // We now create a URI for the request
  // This will send the request to the server
  const String bodyJ = "{\"Name\":\"" + body + "\"}";
  const String str = String("POST") + " http://" + host + " HTTP/1.1\r\n" +
                     "Host: " + "80" + "\r\n" +
                     "Content-Length: " + String(bodyJ.length()) + "\r\n" +
                     "Content-Type: application/json\r\n" +
                     "Connection: close\r\n\r\n";
  const String request = str + bodyJ;
  client.print(request);
  Serial.println(request);
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

  Serial.println();
  Serial.println("closing connection");
  return response;
}

void moveServo(String ind) {
    myservo1.write(90 - 80);
    myservo3.write(90 + 80);
    //  myservo3.write(90 + random(-60,61));
    delay(2000);
    myservo1.write(90);
    myservo3.write(90);
    delay(2000);
  for (int i = 0; i < EXECUTE_NUM; i++) {
    for (int j = 0; j < ind.length() / EXECUTE_NUM; j++) {

    }
  }
}
