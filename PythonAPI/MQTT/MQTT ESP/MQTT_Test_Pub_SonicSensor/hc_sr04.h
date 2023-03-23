namespace Sensors {

  class HC_SR04 {

    public:
      HC_SR04(int triggerPin, int echoPin)
        : _triggerPin(triggerPin), _echoPin(echoPin) {

        pinMode(_triggerPin, OUTPUT);
        pinMode(_echoPin, INPUT);
        digitalWrite(_triggerPin, LOW);
      }

    public:
      int measure_distance_cm(void) {
        digitalWrite(_triggerPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(_triggerPin, LOW);
    
        unsigned long duration_us = pulseIn(_echoPin, HIGH);      // Can take in timeout, should we add one?
        int distance_cm = (0.0172 * duration_us);

        if (distance_cm <= 300 && distance_cm > 0) return distance_cm;
        else return -1;
      }

    private:
      int _triggerPin;
      int _echoPin;
  };

};