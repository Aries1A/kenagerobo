#include <ESP32Servo.h>

Servo myservo1, myservo2, myservo3; // 右前, 後ろ, 左前

void setup() {
  Serial.begin(9600);
  myservo1.attach(2); 
  myservo2.attach(4);
  myservo3.attach(18);
}

void loop() {
//  myservo2.write(90 + 40);
//  myservo1.write(90 - 20);
//  delay(1000);
////  myservo2.write(90);
//  myservo1.write(90); 
  delay(1000);
  myservo1.write(90 - 80);
  myservo3.write(90 + 80);
  //  myservo3.write(90 + random(-60,61));
  delay(2000);
  myservo1.write(90);
  myservo3.write(90);
//  delay(2000);
}
