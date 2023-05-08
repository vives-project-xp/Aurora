#include <WiFi.h>
#include "PubSubClient.h" 
#include "Freenove_WS2812_Lib_for_ESP32.h"
#include <ArduinoJson.h>
#include "hc_sr04.h"
#include "config.h"


using namespace Sonic;

#define FIRMWARE_VERSION "v0.1"

// HS SR04 Ultrasonic Sensor Pins
#define TRIGGER_PIN 0
#define ECHO_PIN    1

Sensors::HC_SR04 ultrasonicSensor(TRIGGER_PIN, ECHO_PIN);

// Communications
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 
String mqttClientId = "";

// RGB LED
#define RGB_COUNT     1
#define RGB_PIN       8
#define RGB_CHANNEL   0
String prefix = "Aurora_sensor";
bool isConnected = false;

Freenove_ESP32_WS2812 strip = Freenove_ESP32_WS2812(RGB_COUNT, RGB_PIN, RGB_CHANNEL, TYPE_GRB);

void status_no_communications(void) {
  strip.setLedColorData(0,255,0,0);
  strip.show();
}

void status_wifi_ok(void) {
  strip.setLedColorData(0, 255, 127, 0);
  strip.show();
}

void status_communications_ok(void) {
  strip.setLedColorData(0, 0, 255, 0);
  strip.show();
}

bool connect_to_wifi(void) {
  Serial.print("Connecting to WiFi ");
  Serial.println(Config::WIFI_SSID);

  WiFi.begin(Config::WIFI_SSID, Config::WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Not yet connected ...");
  }

  Serial.println("Connected to WiFi");
  return true;
}

String get_client_id(void) {
  // static long randomId = random(1000,9999);
  String mqttClientId = WiFi.macAddress().substring(9);
  mqttClientId.replace(":", "");
  mqttClientId.toLowerCase();
  mqttClientId = prefix + mqttClientId;    // + String(randomId);
  return mqttClientId;
}

bool connect_to_mqtt_broker(void) {
  mqttClient.setServer(Config::MQTT_BROKER_IP, Config::MQTT_BROKER_PORT);

  if (mqttClient.connect(get_client_id().c_str())) {
    Serial.print("Connected to MQTT Broker as ");
    Serial.println(get_client_id());
  }
  else {
    Serial.println("Connection to MQTT Broker failed ..");
  }

  return mqttClient.connected();
}

void publish_ultrasonic_distance(int distance) {
  String commandTopic = Config::MQTT_BASE_TOPIC;

  char output[128];
  StaticJsonDocument<128> message;

  message["id"] = get_client_id();
  message["distance"] = distance;

  serializeJson(message, output);

  Serial.print("Publishing measurement message ");
  Serial.println(distance);
  String topic = commandTopic + '/' + get_client_id().substring(prefix.length()) + "/dist";
  mqttClient.publish(topic.c_str(), output);
}

void mqtt_subscribe_callback(char *topic, byte *payload, unsigned int length) {
  char message[64];
  if (length >= sizeof(message)) {
    Serial.println("Received MQTT message but it was too large.");
    return;
  }

  memcpy(message, payload, length);
  message[length] = '\0';
  
  Serial.print("Following message arrived @ ");
  Serial.println(topic);
  Serial.println(message);
  Serial.println("---------------------------");

  StaticJsonDocument<128> doc;        // Not sure how much bigger it needs to be than buffer
  deserializeJson(doc, message);

  const char* command = doc["cmd"];
  const char* sensor = doc["sensor"];
  const int count = 1;
  if(String(sensor) == get_client_id().substring(prefix.length())){
    isConnected = true;
    if (!strcmp(doc["cmd"], "measure")) {
      byte distance[count];
      for(byte i = 0; i <count ;i++){
       //distance[i] = ultrasonicSensor.measure_distance_cm();
       distance[i] = measure_distance_cm_new();
        //delayMicroseconds(30);
      }
      
      int dist = distance[0];
      for(int i = 0; i < count;i++){
        if(distance[i] > dist){
          dist = distance[i];
        }
      }
       publish_ultrasonic_distance(dist);
    }
  }
}

int measure_distance_cm_new(){
    digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(ECHO_PIN, HIGH);
  // Calculating the distance
  int distance = duration * 0.0171;
  // Prints the distance on the Serial Monitor
  return distance;
}

void publish_hello_package(void) {
  String helloTopic = Config::MQTT_BASE_TOPIC + "/connect";

  char output[128];
  StaticJsonDocument<128> message;

  message["id"] = get_client_id();

  serializeJson(message, output);

  Serial.println("Publishing hello message");
  mqttClient.publish(helloTopic.c_str(), output);
}

void setup_mqtt_subscriptions(void) {
  mqttClient.setCallback(mqtt_subscribe_callback);

  String clientId = get_client_id();
  String commandTopic = Config::MQTT_BASE_TOPIC + "/" + clientId.substring(prefix.length()) + "/measure";

  mqttClient.subscribe(commandTopic.c_str());
  mqttClient.subscribe((Config::MQTT_BASE_TOPIC + "/" + clientId.substring(prefix.length())+ "/connected").c_str());
}

void setup() {
  Serial.begin(115200);

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  // randomSeed(analogRead(0));

  // Configure RGB Led
  strip.begin();
  strip.setBrightness(10);
  status_no_communications();

  // Configure HS SR04 Ultrasonic Sensor Module pins
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.println("Starting firmware of ESP32-C3 Sonic Module ...");
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
  

  connect_to_wifi();
  connect_to_mqtt_broker();
  setup_mqtt_subscriptions();
}

void loop() {
  // Needs cleanup but for the moment ok
  if (WiFi.status() != WL_CONNECTED) {
    isConnected = false;
    status_no_communications();
    connect_to_wifi();
    delay(1000);
  }
  if (WiFi.status() == WL_CONNECTED && !mqttClient.connected()) {
    isConnected = false;
    status_wifi_ok();
    connect_to_mqtt_broker();
    delay(1000);
  }
  if (WiFi.status() == WL_CONNECTED && mqttClient.connected()) {
    setup_mqtt_subscriptions();
    if(!isConnected){
      publish_hello_package();
      delay(2000);
    }else{
          status_communications_ok();
    }
  }
  // Give client processing time
  mqttClient.loop();
}
