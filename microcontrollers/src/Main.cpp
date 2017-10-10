//
// Created by rosinator on 10/10/17.
//

#include "Wire.h"
#include "Servo.h"

#define ADDRESS 0x60
#define leftPin 2
#define rightPin 3
#define VictorMax 2000
#define VictorMin 1000
#define JoyMax 100
#define JoyMin 100
int left = 0;
int right= 0;

Servo leftDrive;
Servo rightDrive;

long map(long x, long in_min, long in_max, long out_min, long out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void callBack(int numBytes){
    while(Wire.available()){
        Wire.readBytes((char*)left, sizeof(int));
        Wire.readBytes((char*)right, sizeof(int));
    }
}

void setup(){
    Wire.begin(ADDRESS);
    Wire.onReceive(callBack);
    leftDrive.attach(leftPin);
    rightDrive.attach(rightPin);
}
void loop(){
    leftDrive.writeMicroseconds(map(left, JoyMin, JoyMax, VictorMin, VictorMax));
    rightDrive.writeMicroseconds(map(right, JoyMin, JoyMax, VictorMin, VictorMax));
}
