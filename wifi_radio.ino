#include "WiFi.h"
#include "Audio.h"
#include <ArduinoOTA.h>

// ESP32-S3 pins for PCM5102
#define I2S_BCLK 4
#define I2S_LRC  5
#define I2S_DOUT 6

Audio audio;

// Replace with your network credentials
const char* ssid = "DIR-615";
const char* password = "751248281";

// SomaFM Groove Salad
const char* radioUrl = "http://ice1.somafm.com/groovesalad-128-mp3";

void setup() {
    Serial.begin(115200);
    Serial.println("Starting WiFi Radio...");

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("");
        Serial.print("WiFi connected. IP: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("");
        Serial.println("WiFi connection failed. Check credentials.");
    }

    ArduinoOTA.begin();
    audio.setPinout(I2S_BCLK, I2S_LRC, I2S_DOUT);
    audio.setVolume(12); // 0...21
    audio.connecttohost(radioUrl);
}

void loop() {
    ArduinoOTA.handle();
    audio.loop();
}

// Optional callbacks for debug
void audio_info(const char *info){
    Serial.print("info        "); Serial.println(info);
}
void audio_showstation(const char *info){
    Serial.print("station     "); Serial.println(info);
}
void audio_showstreamtitle(const char *info){
    Serial.print("streamtitle "); Serial.println(info);
}
