#include "Button.h"

extern TFT_eSPI tft; // Déclaré dans main.cpp

Button::Button(int xCoord, int yCoord, int l1, int h1, uint16_t color1, const char* command1) {
  x = xCoord;
  y = yCoord;
  l = l1;
  h = h1;
  color = color1;
  command = command1;
  lastState = false;

}

void Button::draw() {
  tft.fillRect(x, y, l, h, color);
}

bool Button::detect(int px, int py) {

  bool isCurrentlyPressed = (x <= px && px <= x + l) && (y <= py && py <= y + h);
  bool justPressed = isCurrentlyPressed && !lastState;
  return justPressed;
}
void Button::updateState(int px, int py) {
  lastState = (x <= px && px <= x + l) && (y <= py && py <= y + h);
}

int Button::getX() { return x; }
int Button::getY() { return y; }
const char* Button :: getCommand(){return command;}


void Button::setColor(uint16_t new_color) {color = new_color; draw(); }
void Button::setX(int newX) { x = newX; }
void Button::setY(int newY) { y = newY; }