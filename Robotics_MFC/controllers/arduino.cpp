#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

int angles[5] = {90, 90, 90, 90, 60};  // Initial angles for servos 1 to 4

void setup() {
  Serial.begin(115200);

  servo1.attach(3);  // Change to the actual pin
  servo2.attach(4);
  servo3.attach(5);
  servo4.attach(6);

  servo1.write(angles[1]);
  servo2.write(angles[2]);
  servo3.write(angles[3]);
  servo4.write(angles[4]);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    int spaceIndex = input.indexOf(' ');
    if (spaceIndex > 0) {
      int servoID = input.substring(0, spaceIndex).toInt();
      int angle = input.substring(spaceIndex + 1).toInt();
      angle = constrain(angle, 0, 180);  // Safety bounds

      if (servoID >= 1 && servoID <= 4) {
        angles[servoID] = angle;

        switch (servoID) {
          case 1: servo1.write(angle); break;
          case 2: servo2.write(angle); break;
          case 3: servo3.write(angle); break;
          case 4: servo4.write(angle); break;
        }

        // Optional feedback
        Serial.print("POS ");
        Serial.print(servoID);
        Serial.print(" ");
        Serial.println(angle);
      }
    }
  }
}
