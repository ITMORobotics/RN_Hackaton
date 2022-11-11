#include <Arduino.h>
#include <DFRobot_HX711.h>

#define IRS_1_PIN A3
#define IRS_2_PIN A2
#define HX_SLK A0
#define HX_DIN A1
DFRobot_HX711 MyScale(HX_DIN, HX_SLK);

const uint8_t filt_N = 25;
float filt_array[filt_N];
uint8_t filt_index = 0;
float filt_scale = 0;
long sum_scale = 0;
long offset = 0;
float scale = 1852;

void update(long value){
  filt_array[filt_index++] = value;
  sum_scale += value;
  filt_scale = (sum_scale/filt_N - offset)/scale;
  filt_index %= filt_N;
  sum_scale -= filt_array[filt_index];
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // MyScale.setCalibration(1852);
  pinMode(IRS_1_PIN, INPUT); // IR Sensor pin INPUT
  pinMode(IRS_2_PIN, INPUT); // IR Sensor pin INPUT
  for(int i = 0; i < filt_N; i++)
  {
    update(MyScale.getValue());
  }
  offset = filt_scale;
}

void loop() {
  // Get the weight of the object
  // float scale = MyScale.readWeight();
  update(MyScale.getValue());
  Serial.print("s ");
  Serial.println(filt_scale);
  int irs_1 = digitalRead(IRS_1_PIN);
  int irs_2 = digitalRead(IRS_2_PIN);
  Serial.print("i0");
  Serial.println(irs_1);
  Serial.print("i1");
  Serial.println(irs_2);
  // delay(200);
}