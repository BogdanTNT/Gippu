#include <Servo.h>
#include <ArduinoJson.h>
#include <MemoryFree.h>

const int servoCount = 6;

struct DataStruct {
  int id;
  int values[servoCount];
} data;

Servo servos[servoCount];
int servoPins[] = { 3, 5, 6, 9, 10, 11 };
int angles[] = { A0, A1, A2, A3, A6, A7 };

int mapServoPotToAngleMin[] = { 59, 57, 24, 31, 24, 26 };
int mapServoPotToAngleMax[] = { 450, 450, 418, 441, 410, 264 };
bool invertServoPos[] = { 1, 1, 0, 0, 0, 0};

bool teachMode = false;
int motorPowerPin = 2;

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < servoCount; i++) {
    pinMode(angles[i], INPUT);
    servos[i].attach(servoPins[i]);
  }
  Serial.begin(9600);

  // data.values[0] = 30;
  // data.values[1] = 160;
  // data.values[2] = 110;
  // data.values[3] = 50;
  // data.values[4] = 90;
  // data.values[5] = 90;


  data.values[0] = 90;
  data.values[1] = 90;
  data.values[2] = 90;
  data.values[3] = 90;
  data.values[4] = 90;
  data.values[5] = 90;


  // data.values[0] = 0; data.values[1] = 0; data.values[2] = 0;
  // data.values[3] = 150; data.values[4] = 90; data.values[5] = 90;

  pinMode(motorPowerPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  delay(1);
  // put your main code here, to run repeatedly:
  ReceiveData();

  if (!teachMode) {
    MoveServos();
    digitalWrite(motorPowerPin, LOW);
  } else {
    digitalWrite(motorPowerPin, HIGH);
  }
  
  // digitalWrite(LED_BUILTIN, LOW);

}

// Function to extract an array from the JSON document
int extractArray(JsonArray array, int* targetArray) {
  int index = 0;
  for (int value : array) {
    targetArray[index] = value;
    index++;
  }
  return index;
}

void ReceiveData() {
  if (Serial.available()) {
    digitalWrite(LED_BUILTIN, HIGH);

    String jsonStr = Serial.readStringUntil('\n');

    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonStr);

    if (error) {
      Serial.print("JSON parsing error: ");
      Serial.println(error.c_str());
      return;
    }

    data.id = doc["id"];

    // data id 0 - Instantly move servo to the provided angles,
    // 1 - signal from the controller app to the arduino to send current values of servo angles. Used to teach the robot to remember the position it is in,
    // 2 - Data sent from the arduino to controller app with the value of angles the robot is currently in
    if (data.id == 0) {
      extractArray(doc["values"], data.values);

      teachMode = false;
      digitalWrite(LED_BUILTIN, LOW);

    }
    if (data.id == 1) {
      teachMode = true;

      int currentAngles[servoCount];

      for (int j = 0; j < 10; j++) {
        for (int i = 0; i < servoCount; i++) {
          // currentAngles[i] = (float)analogRead(angles[i]);
          float servoValue = (float)analogRead(angles[i]);
          currentAngles[i] = servoValue;
          if(invertServoPos[i])
            currentAngles[i] = 180 - abs((servoValue - mapServoPotToAngleMin[i]) / (mapServoPotToAngleMax[i] - mapServoPotToAngleMin[i])) * 180;
          else
            currentAngles[i] = abs((servoValue - mapServoPotToAngleMin[i]) / (mapServoPotToAngleMax[i] - mapServoPotToAngleMin[i])) * 180;
          delay(1);
        }
      }

      // Convert data to JSON string
      char response[128];
      memset(response, 0, sizeof(response));
      StaticJsonDocument<128> responseDoc;
      responseDoc["id"] = 2;

      delay(3);
      JsonArray responseValuesArr = responseDoc.createNestedArray("values");
      for (int i = 0; i < servoCount; i++) {
        responseValuesArr.add(currentAngles[i]);
        delay(1);
      }

      serializeJson(responseDoc, response, sizeof(response));

      Serial.println(response);
      // Serial.println(freeMemory());

    }
  }
}

void MoveServos() {
  for (int i = 0; i < servoCount; i++) {
    servos[i].write(data.values[i]);
  }
}
