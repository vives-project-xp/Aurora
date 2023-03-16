#include <ArduinoMqttClient.h>
#include <WiFi.h>
#include "arduino_secrets.h"

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID
char pass[] = SECRET_PASS;    // your network password

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "broker.emqx.io";
int        port     = 1883;
const char topic[]  = "SENSOR_0";
const char topic2[]  = "SENSOR_1";
const char topic3[]  = "aurora_sensor";
const char topic4[] = "SENSOR_3";

const long interval = 1000;
unsigned long previousMillis = 0;

int sensor = 15;              // the pin that the sensor is atteched to
int state = LOW;             // by default, no motion detected
int val = 0;                 // variable to store the sensor status (value)


const int periodDuration = 2000;
unsigned long lastPeriodStart;

void setup() {
  pinMode(sensor, INPUT);    // initialize sensor as an input
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();

}

void loop() {
  mqttClient.poll();
  val = analogRead(sensor);   // read sensor value
  //Serial.print(val);
  static int lastValue;
  static int currentValue;
  static bool detection = 0;
  currentValue = val;
  /*Serial.print("    ");
    Serial.print(currentValue);
    Serial.print("    ");
    Serial.println(lastValue);*/
  if (currentValue >= (lastValue + 100) || currentValue <= (lastValue - 100))
  {
    if (detection == 0)
    {
      Serial.println("Turn panel on");
    }
    detection = 1;
    //Serial.println("Detection");
    lastPeriodStart = millis();
  }
  else if (millis() - lastPeriodStart >= periodDuration)
  {
    if (detection == 1)
    {
      Serial.println("Turn panel off");
    }
    detection = 0;
  }
  lastValue = currentValue;



  // call poll() regularly to allow the library to send MQTT keep alives which
  // avoids being disconnected by the broker
  static int Rvalue = 0;
  static int Rvalue2 = 1;
  static int Rvalue3 = 2;
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time a message was sent
    previousMillis = currentMillis;

    //record random value from A0, A1 and A2
    Rvalue = Rvalue + 1;
    Rvalue2 = Rvalue2 * 2;
    Rvalue3 = Rvalue3 + 10;

    Serial.print("Sending message to topic: ");
    Serial.println(topic);
    Serial.println(detection);

    Serial.print("Sending message to topic: ");
    Serial.println(topic2);
    Serial.println(Rvalue2);

    Serial.print("Sending message to topic: ");
    Serial.println(topic2);
    Serial.println(Rvalue3);

    // send message, the Print interface can be used to set the message contents
    mqttClient.beginMessage(topic);
    mqttClient.print(detection);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic2);
    mqttClient.print(Rvalue2);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic3);
    mqttClient.print(Rvalue3);
    mqttClient.endMessage();

    Serial.println();
  }
}
