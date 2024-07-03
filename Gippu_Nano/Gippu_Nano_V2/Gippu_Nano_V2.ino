#include <Servo.h>
#include <ArduinoJson.h>

// Number of servos controlled by this program
const int servoCount = 6;

// Structure to store data for each servo
// ---
// The controller recieves what angle should each servo be
// To maintain a certain speed, the app also tells the controller how many steps should each servo do every millisecond
// Alternatively, if a servo has to move very little, the controller spaces its steps very far apart one from another
struct DataStruct {
  int id; // ID of the command received
  int values[servoCount]; // Array to store angle values for each servo
  // int stepSize[servoCount]; // How big should each servo step should be - usually used when a servo has to move a lot for a single position
  // int stepTime[servoCount]; // How much time to wait until each servo should move - usually used when a servo has to move a little for a single position
} data;

// Array of Servo objects
Servo servos[servoCount];
// Physical pin numbers on Arduino where servos are connected
int servoPins[] = { 3, 5, 6, 9, 10, 11 };
// Analog input pins used for servo position sensors
int angles[] = { A0, A1, A2, A3, A6, A7 };

// Minimum and maximum readings expected from the potentiometers
int mapServoPotToAngleMin[] = { 59, 57, 24, 31, 24, 26 };
int mapServoPotToAngleMax[] = { 450, 450, 418, 441, 410, 264 };
// Flag to indicate if servo position should be inverted
bool invertServoPos[] = { 1, 1, 0, 0, 0, 0};


// Boolean to control whether the robot is in teaching mode
bool teachMode = false;
// Pin to control motor power state
int motorPowerPin = 2;

void setup() {
  for (int i = 0; i < servoCount; i++) {
    pinMode(angles[i], INPUT); // Set up analog pins as input
    servos[i].attach(servoPins[i]); // Attach servo objects to servo pins
  }
  Serial.begin(9600); // Begin serial communication at 115200 bps

  // Initialize all servos to 90 degrees
  for(int i = 0; i < servoCount; i++) {
    data.values[i] = 90;
  }

  pinMode(motorPowerPin, OUTPUT); // Set motor power pin as output
  pinMode(LED_BUILTIN, OUTPUT); // Set built-in LED as output
}

void loop() {
  delay(1); // Short delay for stability

  ReceiveData(); // Function to receive and process incoming data

  if (!teachMode) {
    MoveServos(); // Move servos if not in teach mode
    digitalWrite(motorPowerPin, LOW); // Turn off motor power
  } else {
    digitalWrite(motorPowerPin, HIGH); // Enable motor power in teach mode
  }
}

// Function to extract values from a JSON array and store them in targetArray
int extractArray(JsonArray array, int* targetArray) {
  int index = 0;
  for (int value : array) {
    targetArray[index++] = value;
  }
  return index;
}

// Function to receive and parse data from Serial
void ReceiveData() {
  if (Serial.available()) {
    digitalWrite(LED_BUILTIN, HIGH); // Turn on LED when data is received
    String jsonStr = Serial.readStringUntil('\n'); // Read the incoming data as a string
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonStr); // Parse the JSON string
    if (error) { // Check for errors in parsing
      Serial.print("JSON parsing error: ");
      Serial.println(error.c_str());
      return;
    }

    data.id = doc["id"]; // Get the command ID from JSON document

    // data id 0 - Instantly move servo to the provided angles,
    // 1 - signal from the controller app to the arduino to send current values of servo angles. Used to teach the robot to remember the position it is in,
    // 2 - Data sent from the arduino to controller app with the value of angles the robot is currently in
    if (data.id == 0) {
      extractArray(doc["values"], data.values); // If ID is 0, extract servo values from JSON
      // extractArray(doc["stepSize"], data.stepSize); // If ID is 0, extract stepSize from JSON
      // extractArray(doc["stepTime"], data.stepTime); // If ID is 0, extract stepTime from JSON

      teachMode = false; // Exit teach mode
      digitalWrite(LED_BUILTIN, LOW); // Turn off LED
    }
    if (data.id == 1) {
      teachMode = true; // Enable teach mode

      int currentAngles[servoCount]; // Array to store current servo angles

      // Read the current angles from the analog pins, adjust based on calibration, and send back
      for (int i = 0; i < servoCount; i++) {
        float servoValue = analogRead(angles[i]); // Read the current servo position
        // These two lines should be uncommented if servo should be inverted
        // currentAngles[i] = invertServoPos[i] ? 
        //   180 - abs((servoValue - mapServoPotToAngleMin[i]) / (mapServoPotToAngleMax[i] - mapServoPotToAngleMin[i])) * 180 : 
          abs((servoValue - mapServoPotToAngleMin[i]) / (mapServoPotToAngleMax[i] - mapServoPotToAngleMin[i])) * 180;
      }

      char response[128]; // Buffer for response data
      StaticJsonDocument<128> responseDoc; // Create a small JSON document for response
      responseDoc["id"] = 2; // Set response ID to 2
      JsonArray responseValuesArr = responseDoc.createNestedArray("values"); // Create a nested array in JSON document
      for (int i = 0; i < servoCount; i++) {
        responseValuesArr.add(currentAngles[i]); // Add each angle to the JSON array
      }
      serializeJson(responseDoc, response, sizeof(response)); // Serialize JSON document to string
      Serial.println(response); // Send the response over serial
    }
  }
}

// Function to write values to servos based on received data
void MoveServos() {
  for (int i = 0; i < servoCount; i++) {
    servos[i].write(data.values[i]); // Set each servo to its respective value
  }
}
