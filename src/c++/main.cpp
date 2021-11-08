#include<bits/stdc++.h>
#include "helpers.cpp"

using namespace std;
class Coder {
  public:
    double l;
    string text;
    map<char, pair<double, double>> pTable;

    Coder(double length, string inputText, string action) {
      l = length;
      text = inputText;

      if (action.compare("encode") == 0) {
        fillTable(text);
      }
     
    }
    void fillTable(string text) {
      map<char, double> table;
      for (auto c : text) {
        table[c]++; 
      }

      double last = 0;
      for (auto i : table) {
        table[i.first] /= l;
        table[i.first] += last;
        double temp = table[i.first];
        pair<double, double> p(last, temp);
        pTable[i.first] = p;
        last = temp;
      }
    }

    double newPoint(double s, double e, double p) {
      return (e - s)  * p + s;
    }
    
    tuple<string, string> leftShift(
        string binNumber, 
        int amount, 
        string position, 
        string fullNumber = "", 
        tuple<int, int> numberIndex = make_tuple(0,0)
        ) {
      string adder = "";
      if (position.compare("start") == 0) {
        adder = "0";
      } else if (position.compare("end") == 0) {
        adder = "1";
      } else if (position.compare("number") == 0) {
        return make_tuple(
            fullNumber.substr(
              get<0>(numberIndex), get<1>(numberIndex)
            ),
            ""
        );
      }

      for (int i = 0; i < amount; i++)
        binNumber += adder;
        

      return make_tuple(
          binNumber.substr(amount),
          binNumber.substr(0, amount)
      );
    }

   string encode(string text) {
     double start = 0, end = 1;
     int i = 0;
     string outputs = "";

     for (auto c : text) {
       pair<double, double> ranges(pTable[c]);
       double start1 = newPoint(start, end, ranges.first);
       double end1 = newPoint(start, end, ranges.second);
       tuple<double, double, string> t(
           enNormalize(start1, end1)
       );
       start = get<0>(t);
       end = get<1>(t);
       outputs += get<2>(t);
     }

     double result = ((end - start) / 2) + start;
     return outputs + float2bin(result, 100);
     return "";
   }

   tuple<double, double, string> enNormalize(double initStart, double initEnd) {
     string start, end;
     start = float2bin(initStart, 20);
     end = float2bin(initEnd, 20);
     int amount = 0;

     for (int i = 0; i < start.length(); i++) {
       if (start[i] == end[i]) {
         amount++;
       } else {
         break;
       }
     }

     string output;
     if (amount > 0) {
       tuple<string, string> t;
       t = leftShift(start, amount, "start");            
       start = get<0>(t);
       output = get<1>(t);
       
       t = leftShift(end, amount, "end");            
       end = get<0>(t);
     } else {
       return make_tuple(initStart, initEnd, "");
     }
     string PREFIX = "0.";
     return make_tuple(
         bin2float(PREFIX + (string)start),
         bin2float(PREFIX + (string)end),
         output
     );

   }




};


int main() {
  Coder c(5, "hello", "encode");
}

