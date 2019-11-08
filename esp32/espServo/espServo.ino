#include <ESP32Servo.h>

Servo servo1, servo2,servo3;
int servo1Pin = 18;
int servo2Pin = 4;
int servo3Pin = 2;

int minUs = 500;
int maxUs = 2400;

int pos = 0;

void setup() {
  servo1.setPeriodHertz(50);
  servo1.attach(servo1Pin, minUs, maxUs);
  servo2.setPeriodHertz(50);
  servo2.attach(servo2Pin, minUs, maxUs);
  servo3.setPeriodHertz(50);
  servo3.attach(servo3Pin, minUs, maxUs);
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) {
    servo1.write(pos);
    servo2.write(pos);
//    servo3.write(pos);
    delay(5);
  }
  for (pos = 180; pos >= 0; pos -= 1) {
    servo1.write(pos);
    servo2.write(pos);
//    servo3.write(pos);
    delay(5);
  }
    for (pos = 0; pos <= 180; pos += 1) {
    servo1.write(pos);
//    servo2.write(pos);
    servo3.write(pos);
    delay(5);
  }
  for (pos = 180; pos >= 0; pos -= 1) {
    servo1.write(pos);
//    servo2.write(pos);
    servo3.write(pos);
    delay(5);
  }
    for (pos = 0; pos <= 90; pos += 1) {
//    servo1.write(pos);
    servo2.write(pos);
    servo3.write(pos);
    delay(5);
  }
  for (pos = 90; pos >= 0; pos -= 1) {
//    servo1.write(pos);
    servo2.write(pos);
    servo3.write(pos);
    delay(5);
  }
}

