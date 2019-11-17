#include <ESP32Servo.h>

Servo myservo1, myservo2, myservo3; // 右前, 後ろ, 左前
int action = 0 ;

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
  //  myservo2.write(90);
  //  myservo1.write(90);
  //  delay(1000);
  //  myservo1.write(90 - 80);
  //  myservo3.write(90 + 80);
  //  //  myservo3.write(90 + random(-60,61));
  //  delay(2000);
  //  myservo1.write(90);
  //  myservo3.write(90);
  ////  delay(2000);
  Serial.print("action: ");
  Serial.println(action % 12);
  moveServo(action % 12);
  action++;
  delay(1000);
}


void moveServo(int action) {
//  //速度
//  int roll_speed = 90;
//  //前進後退
//  double rot;
//  if (action % 4 == 1 || action % 4 == 2) {
//    rot = 1;
//  } else {
//    rot = -0.3;
//  }
//  //秒数
//  int second;
//  if (action % 2 == 0) {
//    second = 3;
//  } else {
//    second = 2;
//  }
//  //車輪
//  if (action % 12 >= 1 && action % 12 <= 4) {
//    myservo1.write(90 + rot * roll_speed);
//    myservo3.write(90 - rot * roll_speed);
//  }
//  else if (action % 12 >= 5 && action % 12 <= 8) {
//    myservo2.write(90 + rot * roll_speed);
//    myservo3.write(90 - rot * roll_speed);
//  }
//  else {
//    myservo1.write(90 + rot * roll_speed);
//    myservo2.write(90 - rot * roll_speed);
//  }
  if (action == 0){
    myservo1.write(90 + 90);
    myservo2.write(90 - 90);
    delay(3 * 1000);
    }
    else if (action == 1){
      myservo1.write(90 + 50);
      myservo2.write(90 + 50);
      }
  myservo1.write(90);
  myservo2.write(90);
  myservo3.write(90);
//  Serial.print(rot);
//  Serial.print(", ");
//  Serial.print(second);
//  Serial.print(", ");
//  Serial.println(action % 12);

}
