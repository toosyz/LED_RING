// Enable debug prints to serial monitor
#define MY_DEBUG

// Use a bit lower baudrate for serial prints on ESP8266 than default in MyConfig.h
#define MY_BAUD_RATE 115200

// Enables and select radio type (if attached)
//#define MY_RADIO_RF24
//#define MY_RADIO_RFM69
//#define MY_RADIO_RFM95

#define MY_GATEWAY_ESP8266

#define MY_WIFI_SSID "seize the memes of production"
#define MY_WIFI_PASSWORD "19980308"

// Enable UDP communication
//#define MY_USE_UDP  // If using UDP you need to set MY_CONTROLLER_IP_ADDRESS below

// Set the hostname for the WiFi Client. This is the hostname
// it will pass to the DHCP server if not static.
#define MY_HOSTNAME "brutus"

// Enable MY_IP_ADDRESS here if you want a static ip address (no DHCP)
//#define MY_IP_ADDRESS 192,168,178,87

// If using static ip you can define Gateway and Subnet address as well
//#define MY_IP_GATEWAY_ADDRESS 192,168,178,1
//#define MY_IP_SUBNET_ADDRESS 255,255,255,0

// The port to keep open on node server mode
#define MY_PORT 5050

// How many clients should be able to connect to this gateway (default 1)
#define MY_GATEWAY_MAX_CLIENTS 4

#include<stdio.h>

#if defined(MY_USE_UDP)
#include <WiFiUdp.h>
#endif

#include <ESP8266WiFi.h>
#include <MySensors.h>


#define SN "RGB Color switch"
#define SV "1.1"

#define LED_PIN 2      // Arduino pin attached to MOSFET Gate pin
#define FADE_DELAY 10  // Delay in ms for each percentage fade up/down (10ms = 1s full-range dim)
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            2

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      8

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int onoff=1;

bool blinkingDown=true;

int rotationCount=0;
int blinkingCount=0;

int rotationRate=0;
int blinkingRate=0;

int brightness=155;

class Color{
  public:
    int r;
    int g;
    int b;
    Color(int r0, int g0, int b0)
    {
      r=r0;
      g=g0;
      b=b0;
    }
    Color()
    {
      r=0;
      g=0;
      b=0;
    }
    void print()
    {
      Serial.print(r);
      Serial.print("\n");      
      Serial.print(g);
      Serial.print("\n");      
      Serial.print(b);
      Serial.print("\n");
    }
};

Color list[NUMPIXELS];

void rotate()
{
  Color c=list[NUMPIXELS-1];
  for(int i=NUMPIXELS-2; i>=0; i--)
  {
    list[i+1]=list[i];
  }
  list[0]=c;
}

/***
 * Dimmable LED initialization method
 */
void setup()
{
  Serial.begin(115200); 
  // Pull the gateway's current dim level - restore light level upon node power-up
  pixels.begin(); // This initializes the NeoPixel library.
}

void presentation()
{
  // Register the LED Dimmable Light with the gateway
  sendSketchInfo(SN, SV);
}

/***
 *  Dimmable LED main processing loop
 */
void loop()
{
   for(int i=0;i<NUMPIXELS;i++)
   {
    if(onoff) pixels.setPixelColor(i, pixels.Color(list[i].r,list[i].g,list[i].b)); 
    else pixels.setPixelColor(i, pixels.Color(0,0,0));
   }
   if(rotationRate!=0)
   {
    if(rotationCount!=rotationRate) rotationCount++;
    else 
    {
      rotationCount=0;
      rotate();
    }
   }

   if(blinkingRate!=0)
   {
    if(blinkingCount!=blinkingRate) blinkingCount++;
    else 
    {
      blinkingCount=0;
      
      if(brightness==155) blinkingDown=true;
      else if(brightness==0) blinkingDown=false;
      
      if(blinkingDown) brightness--;
      else brightness++;
      pixels.setBrightness(brightness);
    }   
   }
   pixels.show();
}

void receive(const MyMessage &message)
{
    String s=message.getString();
    if(s.length()<4) {
      Serial.print("string length is 0");
      return;
    }
    int ledNumber=(s[0]-'0')*10+(s[1]-'0');
    //if incoming message is a command message, it arrives to set the rotation and the blinking 
    if(ledNumber==99)
    {
      rotationRate=(s[2]-'0')==0?0:(7-s[2]+'0')*300;
      blinkingRate=(s[3]-'0')==0?0:(7-s[3]+'0')*10;
      blinkingCount=0;
      rotationCount=0;
    }
    else if(ledNumber>=NUMPIXELS)
    {
      Serial.print("pixel numbering does not match on both sides!");
      return;
    }
    else 
    {
      String s1=s.substring(3, 5);
      String s2=s.substring(5, 7);
      String s3=s.substring(7, 9);
      Color c(hexStringToInteger(s1), hexStringToInteger(s2), hexStringToInteger(s3));
      list[ledNumber]=c;
    }
}

int hexStringToInteger(String s)
{
    int x=0;
    int len=s.length();
    for(int i=0; i<len; i++)
    {  
      switch(tolower(s[i])){
        case '1':
          x+=1*pow(16, len-i-1);
          break;
        case '2':
          x+=2*pow(16, len-i-1);
          break;
        case '3':          
          x+=3*pow(16, len-i-1);
          break;
        case '4':
          x+=4*pow(16, len-i-1);
          break;
        case '5':
          x+=5*pow(16, len-i-1);
          break;
        case '6':
          x+=6*pow(16, len-i-1);
          break;
        case '7':
          x+=7*pow(16, len-i-1);
          break;
        case '8':
          x+=8*pow(16, len-i-1);
          break;
        case '9':
          x+=9*pow(16, len-i-1);
          break;
        case 'a':
          x+=10*pow(16, len-i-1);
          break;
        case 'b':
          x+=11*pow(16, len-i-1);
          break;
        case 'c':
          x+=12*pow(16, len-i-1);
          break;
        case 'd':
          x+=13*pow(16, len-i-1);
          break;
        case 'e':
          x+=14*pow(16, len-i-1);
          break;
        case 'f':
          x+=15*pow(16, len-i-1);
          break;
        default: break;
       }
    }
    return x;
}
