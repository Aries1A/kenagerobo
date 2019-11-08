#include <ESP32Servo.h>
Servo myservo;

void setup() {
  Serial.begin(9600);
  myservo.attach(14);
  myservo.write(90 - 180);
}

void loop() {

  delay(10000);
  //  myservo.write(90 + 90);
  //  delay(10000);
}
