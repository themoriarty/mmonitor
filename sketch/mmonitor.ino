#include <LiquidCrystal.h>

#include <SPI.h>
#include <Ethernet.h>
#include "myconfig.h"

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

EthernetClient client;

void setup() {                
  // initialize the digital pin as an output.
  // Pin 13 has an LED connected on most Arduino boards:
  Serial.begin(9600);
  //pinMode(13, OUTPUT);
  Ethernet.begin(mac, my_ip);
  lcd.begin(16, 1);
  lcd.setCursor(0, 0);
}

void send(EthernetClient& client, const char* data)
{
  for (const char* c = data; *c; ++c)
  {
    client.write(*c);
  }
}
char read(EthernetClient& client)
{
  while (!client.available())
  {
    delay(100);
  }
  return client.read();
}

void loop() {
  /*
  digitalWrite(13, HIGH);   // set the LED on
  delay(1000);              // wait for a second
  digitalWrite(13, LOW);    // set the LED off
  delay(1000);              // wait for a second
  Serial.println("blah");
  */
  if (client.connect(server_address, 8123))
    {
      send(client, "GET /result.txt HTTP/1.0\r\n\r\n");
      char pattern[] = "\r\n\r\n";
      byte idx = 0;
      bool body_found = false;
      while (client.connected())
      {
        char c = read(client);
        if (body_found && c >= ' ')
        {
          lcd.write(c);
        }
        if (c == pattern[idx])
        {
          idx++;
        } else
        {
          idx = 0;
        }
        if (idx == sizeof(pattern) / sizeof(pattern[0]) - 1)
        {
          body_found = true;
          lcd.clear();
        }
      }
    }
    else
    {
      Serial.println("can't connect");
    }
  client.stop();
  delay(1000 * 30);  
}
