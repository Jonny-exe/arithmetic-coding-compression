#include<bits/stdc++.h>

using namespace std;
typedef long double LD;

string float2bin(LD number, int places = 200) {
  LD rest, b;
  rest = 0;
  b = 1;
  int i = 1;
  string result = "";

  while (i < places) {
    b = pow(2, -i);
    if (b + rest <= number) {
      result += "1";
      rest += b;
    } else {
      result += "0";
    }
    i++;
  }
  return result;
}

LD bin2float(string number) {
  LD result = 0;
  number = number.substr(number.find(".") + 1);
  for (int i = 0; i < number.length(); i++) {
    char c = number[i];
    if (c == '1')
      result += pow((LD)2, (LD)-(i + 1));
  }
  return result;
}
