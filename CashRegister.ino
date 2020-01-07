#define SIZE_OUT 4
#define SIZE_IN 9
#define BAUD_RATE 9600

const int outPins[SIZE_OUT] = {32, 33, 25, 26};
const int inPins[SIZE_IN]  = {34, 35, 27, 14, 12, 13, 22, 23, 21};

int const size_map = SIZE_OUT * SIZE_IN;

/*char *serial_key[] = {
  "0", "00", ".", "+", "CA/AMTTEND",
  "1", "2", "3", "-", "SUB TOTAL", "MD/ST",
  "4", "5", "6", "x", "CH", "CHK/NS",
  "7", "8", "9", "% 9 4", "10 5", "RA/T/S1", "PO/T/S2",
  "FEED", "X/For/DATETIME", "C AC", "-/ERRCORR", "PLU", "#/DEPTSHIFT", "%/CLK#"
};*/

const uint8_t map_values[size_map] = {
 26,  6, 19, 127,  7, 13, 14,  1,  2,
 16, 23, 29, 127, 15, 22, 30, 10, 127,
  8,  9, 28, 127, 27, 21, 20,  3,  4,
  5, 11, 25, 24, 12, 17, 18, 127,  0
};

int map_toggle[size_map];

void setup() {
  for (int i = 0; i < SIZE_IN; i++){
    pinMode(inPins[i], INPUT_PULLDOWN);
  } 
  for (int i = 0; i < SIZE_OUT; i++){
    pinMode(outPins[i], OUTPUT);
    digitalWrite(outPins[i], LOW);
  }
  Serial.begin(BAUD_RATE);
  delay(100);
}

int val = 0;
int map_index = 0;
void loop() {
  for (int j_out = 0; j_out < SIZE_OUT; j_out++)
  {
    digitalWrite(outPins[j_out], HIGH);
    for (int i_in = 0; i_in < SIZE_IN; i_in++)
    {
      val = digitalRead(inPins[i_in]);
      map_index = (j_out * SIZE_IN) + i_in;
      if (val == map_toggle[map_index])
      {
        continue;
      } else {
        if (val)
        {
          //sprintf(hex_return,"%02X", map_values[map_index]);
          Serial.println(map_values[map_index]);
        }
        map_toggle[map_index] = val;
      }
    }
    digitalWrite(outPins[j_out], LOW);
    delay(5);
  }
}
