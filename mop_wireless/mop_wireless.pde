import websockets.*;

import processing.sound.*;

WebsocketClient wsc;

String val;

PVector v1 = new PVector(0,0,0);
PVector v2 = new PVector(0,0,0);

float degree = 0;
float prev_degree = 0;
PFont font;

boolean okuriModori = false;

int soundPlayStart = 0;
int okuriSoundPlayStart = 0;
int modoriSoundPlayStart = 0;

//SoundFile scratchSound;
SoundFile okuriSound;
SoundFile modoriSound;

void setup() {
  size(640, 480);
  
  //okuriSound = new SoundFile(this, "/Users/makoto/Documents/Processing/mop_wireless/Scratch4.mp3");
  okuriSound = new SoundFile(this, "/Users/makoto/Documents/Processing/mop_wireless/okuri.wav");
  modoriSound = new SoundFile(this, "/Users/makoto/Documents/Processing/mop_wireless/modori.wav");
  
  font = createFont("HiraKakuPro-W8", 12);
  textFont(font);
  
  frameRate(9);
  
  //wsc = new WebsocketClient(this, "ws://131.113.136.133:8081");
  wsc = new WebsocketClient(this, "ws://192.168.43.184:8081");
}

void draw() {
  print("distance:");
  println(degree);
  if ( degree-prev_degree > 100 && soundPlayStart + 100 <= millis()) {
    //scratchSound.play();
    soundPlayStart = millis();
    if ( okuriModori ) {
      okuriSound.play();
    } else {
      modoriSound.play();
    }
    okuriModori = !okuriModori;
    textSize(100);
    fill(255);
    textAlign(CENTER, CENTER);
    text("Scratch!!", width/2, height/2);
  } else {
    background(0);
    fill(0);
    rect(0, 0, 640, 480);
  }
  prev_degree = degree;
}

void webSocketEvent(String msg){
  //print("msg:");
  //println(msg);
  JSONObject json = parseJSONObject(msg);
 //print(json.getFloat("SpX"));
 
  v1 = v2;
  //v2 = new PVector(json.getFloat("SpX"), json.getFloat("SpY"), json.getFloat("SpZ"));
  v2 = new PVector(json.getFloat("SpY"), 0, 0);
  //v2 = new PVector(json.getFloat("AcX"), json.getFloat("AcY"), json.getFloat("AcZ"));
  //v2.normalize();
  
  //float a = PVector.angleBetween(v1, v2);
  //degree = degrees(a);
  //degree = PVector.angleBetween(v1, v2);
  degree = v1.dist(v2);
}
