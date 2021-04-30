#include <DHT_U.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
int incomingByte = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
}

//void loop() {
//  // put your main code here, to run repeatedly:
//  float h = dht.readHumidity();
//  float t = dht.readTemperature();
//  float hi = dht.computeHeatIndex(t, h, false);
//  if (isnan(h) || isnan(t)){
//    Serial.println("Failed to read from DHT");
//  }else{
//    Serial.print(t);Serial.print(",");Serial.print(h);
//    Serial.println();
//    //Serial.print("Feels like: ");
//    //Serial.print(hi);
//  }
//  delay(5000);
//}

void sendData(){
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float hi = dht.computeHeatIndex(t, h, false);
  if (isnan(h) || isnan(t)){
    Serial.println("Failed to read from DHT");
  }else{
    Serial.print(t);Serial.print(",");Serial.print(h);
    Serial.println();
    //Serial.print("Feels like: ");
    //Serial.print(hi);
  }  
}

void loop(){
  if (Serial.available() > 0){
    incomingByte = Serial.read();
    if (incomingByte == 'a' ){
      sendData(); 
    }
  }
}
