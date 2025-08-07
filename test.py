#include <TFT_eSPI.h>
#include "Button.h"

#define TFT_BL 21
#define TOUCH_X_MIN 5     // raw Y
#define TOUCH_X_MAX 239
#define TOUCH_Y_MIN 32    // raw X
#define TOUCH_Y_MAX 307

TFT_eSPI tft = TFT_eSPI();

Button btn1(10,40,93,93,TFT_GREEN,"btn1\n");
Button btn2(113,40,93,93,TFT_GREEN,"btn2\n");
Button btn3(216,40,93,93,TFT_GREEN,"btn3\n");
Button btn4(10,143,93,93,TFT_GREEN,"btn4\n");
Button btn5(113,143,93,93,TFT_GREEN,"btn5\n");
Button btn6(216,143,93,93,TFT_GREEN,"btn6\n");
Button mode_btn(216,0,90,30,TFT_GREEN,"None");

const int btn_nbr = 6;
Button* buttons[btn_nbr] = {&btn1, &btn2, &btn3, &btn4, &btn5, &btn6};

bool mode = true;

int color_compt = 0;
// int last_state_color = 0;
uint16_t color_bg[] = {TFT_GREEN,TFT_PURPLE,TFT_GOLD,TFT_DARKGREY};

String receivedMessage = "";
String chat_messages[10][2] = {{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""}};
int index_chat = 0;

uint16_t hexToTFTColor(String hex) {
  if (hex.charAt(0) == '#') hex.remove(0, 1);

  long number = strtol(hex.c_str(), NULL, 16);
  byte r = (number >> 16) & 0xFF;
  byte g = (number >> 8) & 0xFF;
  byte b = number & 0xFF;

  return tft.color565(r, g, b);
}

void setup() {
  Serial.begin(115200);

  pinMode(TFT_BL, OUTPUT);
  digitalWrite(TFT_BL, HIGH);

  tft.init();
  tft.setRotation(3);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE);
  tft.setTextSize(3);
  tft.setCursor(0, 0);

  
}

void loop() {
  uint16_t rawX, rawY;
  int screenX, screenY;

  if (tft.getTouch(&rawX, &rawY)) {

    //rotation 1
    // screenX = map(rawY, TOUCH_X_MIN, TOUCH_X_MAX, 0, 319);  // rawY devient X écran
    // screenY = map(rawX, TOUCH_Y_MIN, TOUCH_Y_MAX, 0, 239);  // rawX devient Y écran
    //rotation 2 
    screenX = map(rawY, TOUCH_X_MIN, TOUCH_X_MAX, 319, 0);  // Inversé horizontalement
    screenY = map(rawX, TOUCH_Y_MIN, TOUCH_Y_MAX, 239, 0);  // Pas inversé


  }
  else {
    //button update state
    for (int i = 0; i < btn_nbr; i++) {
      buttons[i]->updateState(-1, -1);
    }
    mode_btn.updateState(-1,-1);
    screenX = -100;
    screenY = -100;

  }

  tft.setCursor(0, 0);
  // tft.fillScreen(TFT_BLACK);

  mode_btn.draw();

  if(mode_btn.detect(screenX, screenY)){
    mode = !mode;
    tft.fillScreen(TFT_BLACK);
  //   String chat_messages[10][2] = {{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""},{"",""}};
  // }

  if(mode){
    tft.print("Matheo DECK");

    //draw buttons
    for(int i = 0; i < 6; i++){
      buttons[i] -> draw();
    }

    //buttons detect
    for (int i = 0; i < btn_nbr; i++) {
      if (buttons[i]->detect(screenX, screenY)) {
        buttons[i] -> setColor(TFT_RED);
        Serial.write(buttons[i]->getCommand());
      }
      else{
        buttons[i] -> setColor(color_bg[color_compt]);
      
      }
    }

    // button update state
    for (int i = 0; i < btn_nbr; i++) {
      buttons[i] -> updateState(screenX, screenY);
    }
    mode_btn.updateState(screenX,screenY);

  }
  else{
    tft.setTextSize(3);
    tft.setTextColor(TFT_WHITE);
    tft.print("Twitch chat");

    if (Serial.available()) {
      String input = Serial.readStringUntil('\n');
      input.trim();  // Supprime les espaces ou sauts de ligne

      // Séparer les parties avec le séparateur " | "
      int firstSep = input.indexOf('|');
      int secondSep = input.indexOf('|', firstSep + 1);

      if (firstSep > 0 && secondSep > firstSep) {
        String hexColor = input.substring(0, firstSep);
        hexColor.trim();

        String pseudo = input.substring(firstSep + 1, secondSep);
        pseudo.trim();

        String message = input.substring(secondSep + 1);
        message.trim();

       
        for (int i = 10 - 1; i > 0; --i) {
          for (int j = 0; j < 2; ++j) {
            chat_messages[i][j] = chat_messages[i - 1][j];
          }
        }
        chat_messages[0][0] = hexColor; 
        String txt = pseudo + ": " + message;
        chat_messages[0][1] = txt; // Store the message in the array
        //max 13


       
        tft.fillScreen(TFT_BLACK);
        tft.setTextSize(2);

        int y = 30;
        int maxWidth = tft.width() - 4; // 2px margin left/right
        for(int i = 0; i < 10; i++){
          if(chat_messages[i][0] != ""){
            tft.setTextColor(hexToTFTColor(chat_messages[i][0]));
            String msg = chat_messages[i][1];
            int start = 0;
            int msgLen = msg.length();
            while (start < msgLen) {
              int len = 0;
              int px = 0;
              // Find max substring that fits in maxWidth
              while (start + len < msgLen) {
                String sub = msg.substring(start, start + len + 1);
                px = tft.textWidth(sub);
                if (px > maxWidth) break;
                len++;
              }
              if (len == 0) len = 1; // Always print at least one char
              tft.setCursor(2, y); // 2px margin left
              tft.print(msg.substring(start, start + len));
              y += 20;
              start += len;
            }
            y += 4;
          }
        }

        // tft.setCursor(0, 30);

        // tft.print(txt);
        

      }
      
    }
    mode_btn.updateState(screenX,screenY);

  }
}
  



