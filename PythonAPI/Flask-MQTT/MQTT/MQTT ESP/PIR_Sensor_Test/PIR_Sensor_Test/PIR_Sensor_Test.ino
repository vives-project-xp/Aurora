int sensor = 15;              // the pin that the sensor is atteched to
int state = LOW;             // by default, no motion detected
int val = 0;                 // variable to store the sensor status (value)


const int periodDuration = 2000;

unsigned long lastPeriodStart;

void setup() {
  pinMode(sensor, INPUT);    // initialize sensor as an input
  Serial.begin(9600);        // initialize serial
  Serial.print("Setup complete");
}

void loop() {
  val = analogRead(sensor);   // read sensor value
  //Serial.print(val);
  static int lastValue;
  static int currentValue;
  static int detection = 0;
  currentValue = val;
 /* Serial.print("    ");
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
}
