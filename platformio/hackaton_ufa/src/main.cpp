#include <Arduino.h>
#include <DFRobot_HX711.h>

#define IRS_1_PIN A3
#define IRS_2_PIN A2
#define HX_SLK A0
#define HX_DIN A1
DFRobot_HX711 MyScale(HX_DIN, HX_SLK);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  MyScale.setCalibration(1852);
  pinMode(IRS_1_PIN, INPUT); // IR Sensor pin INPUT
  pinMode(IRS_2_PIN, INPUT); // IR Sensor pin INPUT
}

void loop() {
  // Get the weight of the object
  // float scale = MyScale.readWeight();
  float scale = MyScale.getValue();
  Serial.print("s ");
  Serial.println(scale);
  int irs_1 = digitalRead(IRS_1_PIN);
  int irs_2 = digitalRead(IRS_2_PIN);
  Serial.print("i0");
  Serial.println(irs_1);
  Serial.print("i1");
  Serial.println(irs_2);
  // delay(200);
}