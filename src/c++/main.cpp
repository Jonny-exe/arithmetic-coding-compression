#include<bits/stdc++.h>
#include "helpers.cpp"


typedef map<char, pair<double, double>> ttable;
using namespace std;
class Coder {
  public:
    double l;
    string text;
    string output;
    ttable pTable;

    Coder(double length, string inputText, string action, ttable table = {}) {
      pTable = table;
      l = length;
      text = inputText;

      if (action.compare("encode") == 0) {
        fillTable(text);
        output = encode(text);
      } else if (action.compare("decode") ==  0) {
        output = decode(text, pTable);
      } else {
        cout << "Action value is not valid";
      }
    }

    void fillTable(string text) {
      map<char, double> table;
      for (auto c : text) {
        table[c]++; 
      }

      double last = 0;
      for (auto i : table) {
        table[i.first] /= (double)l;
        table[i.first] += last;
        double temp = table[i.first];
        pair<double, double> p(last, temp);
        pTable[i.first] = p;
        cout << i.first << " " << p.first << " " << p.second << endl;
        last = temp;
      }
    }

    double newPoint(double s, double e, double p) {
      return (e - s) * p + s;
    }
    
    tuple<string, string> leftShift(
        string binNumber, 
        int amount, 
        string position, 
        string fullNumber = "", 
        pair<int, int> numberIndex = make_pair(0,0)
        ) {
      string adder = "";
      if (position.compare("start") == 0) {
        adder = "0";
      } else if (position.compare("end") == 0) {
        adder = "1";
      } else if (position.compare("number") == 0) {
        return make_tuple(
            fullNumber.substr(
              numberIndex.first, numberIndex.second
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
       cout << ranges.first << " " << ranges.second << endl;
       double start1 = newPoint(start, end, ranges.first);
       double end1 = newPoint(start, end, ranges.second);
       cout << start1 << " " << end1 << endl;
       tuple<double, double, string> t(
           enNormalize(start1, end1)
       );
       start = get<0>(t);
       end = get<1>(t);
       outputs += get<2>(t);
     }

     double result = ((end - start) / (double)2) + start;
     return outputs + float2bin(result, 100);
   }
   
   string decode(
       string encodedString, 
       map<char, pair<double, double>> table
   ) {
     string fullEncoded = encodedString;
     pair<int, int> encodedIdx(0, 300);
     string encodedNumber = "0." + encodedString.substr(
         encodedIdx.first, encodedIdx.second);
     double encoded = bin2float(encodedNumber);
     double start, end;
     start = 0;
     end = 1;
     int i = 0;
     string decoded = "";
     while (i < l) {
       for (auto i : table) {
         double s, e;
         s = i.second.first;
         e = i.second.second;
         double bigger = newPoint(start, end, s);
         double smaller = newPoint(start, end, e);
         if (encoded >= bigger && encoded < smaller) {
           decoded += i.first;
           double start1, end1;
           start1 = newPoint(start, end, s);
           end1 = newPoint(start, end, e);
           tuple<double, double, double, pair<int, int>> t;
           t = deNormalize(
               start1,
               end1, 
               encoded,
               fullEncoded,
               encodedIdx
           );
           start = get<0>(t);
           end = get<1>(t);
           encoded = get<2>(t);
           encodedIdx = get<3>(t);
           break;
         }

       }
       i++;
     }
     return decoded;
   }

   tuple<double, double, double, pair<int, int>> deNormalize(
       double initStart, 
       double initEnd, 
       double initNumber, 
       string fullNumber, 
       pair<int, int> numberIndex
       ) {
     string start, end, number;
     start = float2bin(initStart, 20);
     end = float2bin(initEnd, 20);
     number = float2bin(initNumber, 20);
     int amount = 0;
     for (int i = 0; i < start.length(); i++) {
       if (start[i] == end[i] && start[i] == number[i])
         amount++;
       else
         break;
     }

     if (amount > 0) {
       if (numberIndex.second + amount < l) {
         numberIndex = make_pair(
             numberIndex.first + amount, 
             numberIndex.second + amount
         );
       }

       start = get<0>(leftShift(start, amount, "start"));
       end = get<0>(leftShift(end, amount, "end"));
       number = get<0>(leftShift(number, amount, "end", fullNumber=fullNumber, numberIndex=numberIndex));

     } else {
       return make_tuple(initStart, initEnd, initNumber, numberIndex);
     }
     string PREFIX = "0.";
     return make_tuple(
         bin2float(PREFIX + start),
         bin2float(PREFIX + end),
         bin2float(PREFIX + number),
         numberIndex
         );
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
         bin2float(PREFIX + start),
         bin2float(PREFIX + end),
         output
     );

   }
};


int main() {
  string text =  "asdfasdf";
  Coder en(text.length(), text, "encode");
  string out = en.output;
  cout << "output: " << out << endl;
  Coder de(out.length(), out, "decode", en.pTable);
  cout << "output: " << de.output << endl;

}

