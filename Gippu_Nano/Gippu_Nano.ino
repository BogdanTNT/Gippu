#include <Servo.h>
#include <ArduinoJson.h>

const int servoCount = 6;

struct DataStruct {
  int id;
  int values[servoCount];
} data;

Servo servos[servoCount];
int servoPins[] = { 3, 5, 6, 9, 10, 11};
int angles[] = { A0, A1, A2, A3, A6, A7};

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < servoCount; i++) {
    pinMode(angles[i], INPUT);
    servos[i].attach(servoPins[i]);
  }
  Serial.begin(9600);

  data.values[0] = 0; data.values[1] = 130; data.values[2] = 110;
  data.values[3] = 180; data.values[4] = 90; data.values[5] = 90;
}

void loop() {
  // put your main code here, to run repeatedly:
  ReceiveData();

  MoveServos();
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
    String jsonStr = Serial.readStringUntil('\n');

    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonStr);

    if (error) {
      Serial.print("JSON parsing error: ");
      Serial.println(error.c_str());
      return;
    }

    data.id = doc["id"];
    extractArray(doc["values"], data.values);

    // data id 0 - move servo, 
    // 1 - send servo angle to controller, 
    // 2 - sent angle values to controller
    if(data.id == 1) {
      for(int i = 0 ; i < servoCount; i++) {
        data.values[i] = analogRead(angles[i]) / 1024 * 180;
      }

      // Convert data to JSON string
      char response[128];
      memset(response, 0, sizeof(response));
      StaticJsonDocument<128> responseDoc;
      responseDoc["id"] = 2;

      JsonArray responseValuesArr = responseDoc.createNestedArray("values");
      for (int i = 0; i < 6; i++) {
        responseValuesArr.add(data.values[i]);
      }
      
      serializeJson(responseDoc, response, sizeof(response));

      Serial.println(response);
    }
  }
}

void MoveServos() {
  for (int i = 0; i < servoCount; i++) {
    servos[i].write(data.values[i]);
  }
}