/* Analog Read to LED
 * ------------------ 
 *
 * turns on and off a light emitting diode(LED) connected to digital  
 * pin 13. The amount of time the LED will be on and off depends on
 * the value obtained by analogRead(). In the easiest case we connect
 * a potentiometer to analog pin 2.
 *
 * Created 1 December 2005
 * copyleft 2005 DojoDave <http://www.0j0.org>
 * http://arduino.berlios.de
 *
 */

#include <AFMotor.h>
     
AF_DCMotor motor(1, MOTOR12_1KHZ); // create motor #2, 64KHz pwm

int potPin = 2;    // select the input pin for the potentiometer
int ledPin = 13;   // select the pin for the LED
int valf = 0;       // variable to store the value coming from the sensor
int valb = 0;       // variable to store the value coming from the sensor
int val = 0;       // variable to store the value coming from the sensor

void setup() {
  pinMode(ledPin, OUTPUT);  // declare the ledPin as an OUTPUT
  Serial.begin(9600);
  motor.setSpeed(200); // set the speed to 200/255. If the speed is too slow, it does not move !
}

void gotox(int x){
// Move m,otorized slider till it reaches the exact position.
//   
// Forward goes towards 0, Backward goes toward max

int slack = 5;

val = analogRead(potPin);    // read the value from the sensor
while (val < x-slack || val > x+slack)
{
  if (x>val){
    motor.run(BACKWARD); // turn it on going forward
  }
  else if (x<val){
    motor.run(FORWARD); // turn it on going forward
  }
  delay(1);
  val = analogRead(potPin);    // read the value from the sensor
}

motor.run(RELEASE);

}

void loop() {
  int i;
  
  Serial.print("tick");
  motor.run(FORWARD); // turn it on going forward
  delay(1000);
  valf = analogRead(potPin);    // read the value from the sensor
  motor.run(BACKWARD); // turn it on going forward
  delay(1000);
  valb = analogRead(potPin);    // read the value from the sensor
  motor.run(RELEASE);
  delay(1000);
  //digitalWrite(ledPin, HIGH);  // turn the ledPin on
  delay(10);                  // stop the program for some time
  Serial.print("Val Forward ");
  Serial.print(valf);
  Serial.print("\n");
  Serial.print("Val Backward ");
  Serial.print(valb);
  Serial.print("\n");
  
  motor.run(FORWARD); // Go forward for 0
  delay(1000);
  for (i=0;i<8;i++){    
    gotox(i*100);
    delay(1000);
  }
  //digitalWrite(ledPin, LOW);   // turn the ledPin off
  delay(10);                  // stop the program for some time
}
