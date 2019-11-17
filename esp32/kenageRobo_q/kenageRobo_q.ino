#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <ESP32Servo.h>
#include <Math.h>
#include "Wire.h"

int16_t mx, my, mz;

Servo myservo1, myservo2, myservo3; // 右前, 後ろ, 左前

const char* ssid = "elecom2g-c08850"; //サーバーのSSID
const char* password = "3A7344CE7169FD2122B9F397AA3EB79F212E5E0741AEF3BB5A5E6BC652F15C0F"; //サーバーのパスワード
//const char* ssid = "ist_members"; //サーバーのSSID
//const char* password = "8gAp3nY!s2Gm"; //サーバーのパスワード
//const char* ssid="Prototyping & Design Lab. 5GHz"; //サーバーのSSID
//const char* pass=""; //サーバーのパスワード

const char* host = "192.168.2.100";
//const char* host = "157.82.207.143";

//const int IND_NUM = 10;
//const int EXECUTE_NUM = 3;
const int STEP_MAX = 100;
int state, angle;
int action;
int steps = 0;
int episode = 0;
int Qsteps;
String action_steps[2] = {"\0"};

String postToServer(String Name = "", String Data = " ");

void setup() {
  Wire.begin(); //これ重要！！
  Serial.begin(115200);
  setupMPU9255();
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(100);
    ESP.restart();
  }
  //  WiFi.config(IPAddress(157, 82, 207, 142), WiFi.gatewayIP(), WiFi.subnetMask());
  //  WiFi.config(IPAddress(192, 168, 2, 107), WiFi.gatewayIP(), WiFi.subnetMask());
  Serial.println(WiFi.localIP());

  state = 0;
  myservo1.attach(2);
  myservo2.attach(4);
  myservo3.attach(18);
  //  postToServer("_reset", String(steps));
  postToServer("set_espStep", String(steps));
  postToServer("set_angle", String(angle));
}

//実行
void execute(int state) {
  action_steps[0] = "\0";
  action_steps[1] = "\0";

  if (state == 0) {
    delay(1000);
  }
  else if (state == 1) {
    //動作
    moveServo(action);
  }
  else if (state == 2) {
    //測位待機
    angle = readCompass();
    delay(300);
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
    int episodeStart = postToServer("get_episodeStart").toInt();
    if (episodeStart == 0) {
      Serial.println("not ready");
      angle = readCompass();
      state = 0;
    }
    //取得
    else {
      String action_steps_tmp = postToServer("get_action_step");
      split(action_steps_tmp, ',', action_steps);
      action = action_steps[0].toInt();
      steps = action_steps[1].toInt();
      if (action == -1) {
        ESP.restart();
      }
      Serial.println("action start");
      state = 1;
    }
  }
  else if (currentstate == 1) {
    //動作終了
    steps++;
    postToServer("set_espStep", String(steps));
    postToServer("set_angle", String(angle));
    Serial.print("Current steps: ");
    Serial.println(String(steps));
    state = 2;
  }
  else if (currentstate == 2) {
    String action_steps_tmp = postToServer("get_action_step");
    split(action_steps_tmp, ',', action_steps);
    action = action_steps[0].toInt();
    Qsteps = action_steps[1].toInt();
    if (action == -1) {
      ESP.restart();
    }
    if (steps != Qsteps) {
      if (steps % STEP_MAX == Qsteps || steps > STEP_MAX) {
        Serial.println("next episode");
        steps = 0;
        state = 0;
        episode++;
      }
      else {
        Serial.println("no action yet");
        state = 2;
      }
    }
    else {
      Serial.println("next step");
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
    state = 0;
  }
}



void loop() {
  //  ArduinoOTA.handle();
  Serial.println("Current State is " + String(state));
  execute(state);
}

//ここから便利ツール的関数
//split関数
int split(String data, char delimiter, String * dst) {
  int index = 0;
  int arraySize = (sizeof(data) / sizeof((data)[0]));
  int datalength = data.length();
  //今回だけ
  dst[0] = "";
  dst[1] = "";
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
String postToServer(String Name, String Data) {
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

//void moveServo(int action) {
//  myservo1.write(90 + 80);
//  myservo3.write(90 - 80);
//  //  myservo3.write(90 + random(-60,61));
//  delay(2000);
//  myservo1.write(90);
//  myservo3.write(90);
//  delay(2000);
//}


void moveServo(int action) {
  //速度
  int roll_speed = 90;
  //前進後退
  double rot;
  if (action % 4 == 1 || action % 4 == 2) {
    rot = 1;
  } else {
    rot = -0.5;
  }
  //秒数
  int second;
  if (action % 2 == 0) {
    second = 3;
  } else {
    second = 2;
  }
  //車輪
  if (action % 12 >= 1 && action % 12 <= 4) {
    myservo1.write(90 + rot * roll_speed);
    myservo3.write(90 - rot * roll_speed);
  }
  else if (action % 12 >= 5 && action % 12 <= 8) {
    myservo2.write(90 + rot * roll_speed);
    myservo3.write(90 - rot * roll_speed);
  }
  else {
    myservo1.write(90 + rot * roll_speed);
    myservo2.write(90 - rot * roll_speed);
  }
  delay(second * 1000);
  myservo1.write(90);
  myservo2.write(90);
  myservo3.write(90);
  Serial.print(rot);
  Serial.print(", ");
  Serial.print(second);
  Serial.print(", ");
  Serial.println(action % 12);
}

int readCompass() {
  Wire.beginTransmission(0x0C);
  Wire.write(0x02);
  Wire.endTransmission();
  Wire.requestFrom(0x0C, 1);

  uint8_t ST1 = Wire.read();
  if (ST1 & 0x01) {
    Wire.beginTransmission(0x0C);
    Wire.write(0x03);
    Wire.endTransmission();
    Wire.requestFrom(0x0C, 7);
    uint8_t i = 0;
    uint8_t buf[7];
    while (Wire.available()) {
      buf[i++] = Wire.read();
    }
    if (!(buf[6] & 0x08)) {
      mx = ((int16_t)buf[1] << 8) | buf[0];
      my = ((int16_t)buf[3] << 8) | buf[2];
      mz = ((int16_t)buf[5] << 8) | buf[4];
    }
  }
  mx -= -82;
  my -= 94;
  mz -= 8;
  mx -= 16;
  my -= -18;
  mz -= -6;
  int angle = atan2(mx, my) / M_PI / 2 * 360 + 180 + 90;
  //    String Data = String(mx) + "," + String(my) + "," + String(mz);
  if (angle > 360) {
    angle -= 360;
  }
  Serial.println(angle);
  return angle;
}

void setupMPU9255() {
  Wire.beginTransmission(0x68);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission();

  Wire.beginTransmission(0x68);
  Wire.write(0x1A);
  Wire.write(0x05);
  Wire.endTransmission();

  Wire.beginTransmission(0x68);
  Wire.write(0x37);
  Wire.write(0x02);
  Wire.endTransmission();

  Wire.beginTransmission(0x0C);
  Wire.write(0x0A);
  Wire.write(0x16);
  Wire.endTransmission();
  delay(500);
}
