#include <Servo.h>

Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;
Servo servo8;
Servo servo9;

int neutral = 1500;
int down = 1600;
int up = 1400;
int power = 1750;
int powerup = 1250;
int pins[8] = {2, 3, 4, 5, 6, 7, 8, 9};

void setup() {
    //Serial.begin(9600);
    delay(3000);
    servo2.attach(2);
    servo3.attach(3);
    servo4.attach(4);
    servo5.attach(5);
    servo6.attach(6);
    servo7.attach(7);
    servo8.attach(8);
    servo9.attach(9);
    neut();
}

void loop() {
    forward();
    neut();
    dive();
    neut();
    delay(1000);
    hoverspin();
    neut();
    hoverforward();
    neut();
    forward();
    neut();
    delay(3000);
}

void surface() {
    servo6.writeMicroseconds(power);
    servo7.writeMicroseconds(powerup);
    servo8.writeMicroseconds(powerup);
    servo9.writeMicroseconds(power);
    delay(6000);
}

void neut() {
    servo2.writeMicroseconds(neutral);
    servo3.writeMicroseconds(neutral);
    servo4.writeMicroseconds(neutral);
    servo5.writeMicroseconds(neutral);
    servo6.writeMicroseconds(neutral);
    servo7.writeMicroseconds(neutral);
    servo8.writeMicroseconds(neutral);
    servo9.writeMicroseconds(neutral);
    delay(500);
    
}

void forward() {
    servo2.writeMicroseconds(power);
    servo3.writeMicroseconds(powerup);
    delay(1500);
}

void dive() {
    servo6.writeMicroseconds(powerup+25);
    servo7.writeMicroseconds(power-25);
    servo8.writeMicroseconds(power-25);
    servo9.writeMicroseconds(powerup+25);
    delay(3000);
}

void diveForward() {
    servo6.writeMicroseconds(powerup);
    servo7.writeMicroseconds(power-50);
    servo8.writeMicroseconds(power-50);
    servo9.writeMicroseconds(powerup);
    servo2.writeMicroseconds(power);
    servo3.writeMicroseconds(powerup);
    delay(6000);   
}

void spin() {
     servo2.writeMicroseconds(powerup);
    servo3.writeMicroseconds(powerup);
    delay(3000);
}

void hoverspin() {
    servo2.writeMicroseconds(powerup);
    servo3.writeMicroseconds(powerup);
    servo6.writeMicroseconds(powerup+25);
    servo7.writeMicroseconds(power-25);
    servo8.writeMicroseconds(power-25);
    servo9.writeMicroseconds(powerup+25);
    delay(1000);
}

void hoverforward() {
    servo2.writeMicroseconds(power);
    servo3.writeMicroseconds(powerup);
    servo6.writeMicroseconds(powerup+25);
    servo7.writeMicroseconds(power-25);
    servo8.writeMicroseconds(power-25);
    servo9.writeMicroseconds(powerup+25);
    delay(3500);
    
}
