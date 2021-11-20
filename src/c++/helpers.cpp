#include<bits/stdc++.h>
using namespace std;
string float2bin(double number, int places = 200) {
  double rest, b;
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

double bin2float(string number) {
  double result = 0;
  number = number.substr(number.find(".") + 1);
  for (int i = 0; i < number.length(); i++) {
    char c = number[i];
    if (c == '1')
      result += pow(2, -(i + 1));
  }
  return result;
}

//int main() {
  /*
  cout << "Test: " << endl;

  double number = 0.75;
  cout << bin2float("0.11") << endl;
  cout << float2bin(number, 20) << endl;
  */
//}
