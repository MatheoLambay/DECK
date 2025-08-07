#ifndef BUTTON_H
#define BUTTON_H

#include <TFT_eSPI.h>

class Button {
  private:
    int x;
    int y;
    int h;
    int l;
    uint16_t color;
    const char* command;
    bool lastState;

  public:
    Button(int xCoord, int yCoord, int l1, int h1, uint16_t color1, const char* command1);
    void draw();
    bool detect(int px, int py);
    int getX();
    int getY();
    void setX(int newX);
    void setY(int newY);
    const char* getCommand();
    void setColor(uint16_t new_color);
    void updateState(int px, int py);    
};

#endif