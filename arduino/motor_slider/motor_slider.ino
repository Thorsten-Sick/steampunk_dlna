#include <AFMotor.h>
#include <Servo.h> 

     
AF_DCMotor slider(1, MOTOR12_1KHZ); // create motor #2, 64KHz pwm
AF_Stepper stepper(48, 2);  // 48 is right for this guy: http://www.tinkersoup.de/small-stepper-motor/a-664/

Servo servo1;
Servo servo2;


int potPin = 2;    // select the input pin for the potentiometer
//int ledPin = 13;   // select the pin for the LED
int valf = 0;       // variable to store the value coming from the sensor
int valb = 0;       // variable to store the value coming from the sensor
int val = 0;       // variable to store the value coming from the sensor

void setup() {
  servo1.attach(10);
  servo2.attach(9);
  

  Serial.begin(9600);
  slider.setSpeed(200); // set the speed to 200/255. If the speed is too slow, it does not move !
  stepper.setSpeed(10); // 10 rpm
     
  //stepper.step(10, FORWARD, SINGLE);
  stepper.release();
  delay(1000);
  slider.run(RELEASE);
}


//Servo stuff
/////////////

// Slider stuff
///////////////
void gotox(int x){
// Move m,otorized slider till it reaches the exact position.
//   
// Forward goes towards 0, Backward goes toward max

int slack = 5;

val = analogRead(potPin);    // read the value from the sensor
while (val < x-slack || val > x+slack)
{
  if (x>val){
    slider.run(BACKWARD); // turn it on going forward
  }
  else if (x<val){
    slider.run(FORWARD); // turn it on going forward
  }
  delay(1);
  val = analogRead(potPin);    // read the value from the sensor
}

slider.run(RELEASE);

}

void slider_init(){
  Serial.print("tick");
  slider.run(FORWARD); // turn it on going forward
  delay(1000);
  valf = analogRead(potPin);    // read the value from the sensor
  slider.run(BACKWARD); // turn it on going forward
  valb = analogRead(potPin);    // read the value from the sensor
  slider.run(RELEASE);
  delay(10);
  
  Serial.print("Val Forward ");
  Serial.print(valf);
  Serial.print("\n");
  Serial.print("Val Backward ");
  Serial.print(valb);
  Serial.print("\n");
}

void slider_step(){
  int i;

  gotox(0);
  for (i=0;i<8;i++){    
    gotox(i*100);
    delay(100);
  }
  delay(10);                  // stop the program for some time
}


// Stepper stuff
////////////////

void move_stepper(int dir){
  if (dir<0){
    stepper.step(dir*-1, BACKWARD, SINGLE);
  }
  else{
    stepper.step(dir, FORWARD, SINGLE);
  }
  stepper.release();
}

// Servo stuff
//////////////

void move_servo(int no, int pos){
  if (no == 1){
    servo1.write(pos);
  }
  if (no == 2){
    servo2.write(pos);
  }
}

// Loop
///////
void loop() {
  int value;
  int command;
  
  if (Serial.available() > 0) {
    int command = Serial.read();

    switch (command) {
    case 'c':    // Clock, the stepper
      value = Serial.parseInt();
      move_stepper(value);
      break;
    case 'a':    // Servo a(1)
      value = Serial.parseInt();
      move_servo(1, value);
      break;
    case 'b':    // Servo b
      value = Serial.parseInt();
      move_servo(2, value);
      break;
    default:     
      break;
      }
    }
}
