import processing.sound.*;
import processing.serial.*;

Serial myPort;
String val;

PVector v1 = new PVector(0,0,0);
PVector v2 = new PVector(0,0,0);

float degree = 0;
//float playingStartedAt = 0;
PFont font;

SoundFile scratchSound;

void setup() {
  size(640, 480);
  
  scratchSound = new SoundFile(this, "/Users/makoto/Documents/Processing/mop/Scratch4.mp3");
  
  font = createFont("HiraKakuPro-W8", 12);
  textFont(font);
  
  frameRate(7);
  
  String portName = Serial.list()[3];
  myPort = new Serial(this, portName, 115200);
  myPort.bufferUntil(10); 
}

void draw() {
  println(degree);
  if ( degree > 8 ) {
    //if(millis() - playingStartedAt > scratchSound.duration()) {
    //  background(255);
    //  scratchSound.play();
    //  playingStartedAt = millis();
    //}
    scratchSound.play();
    textSize(100);
    fill(255);
    textAlign(CENTER, CENTER);
    text("Scratch!!", width/2, height/2);
  } else {
    background(0);
    fill(0);
    rect(0, 0, 640, 480);
  }
}

void serialEvent(Serial myPort) {
  val = myPort.readString();
  
  String[] vec = val.split(",");
  
  if (vec.length == 3) {
    v1 = v2;
    //v2 = new PVector(Float.parseFloat(vec[0]), Float.parseFloat(vec[1]), Float.parseFloat(vec[2]));
    v2 = new PVector(Float.parseFloat(vec[0]), Float.parseFloat(vec[1]), 0);
    
    float a = PVector.angleBetween(v1, v2);
    degree = degrees(a);
  }
}
