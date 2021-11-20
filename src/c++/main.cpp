#include<bits/stdc++.h>
#include "helpers.cpp"
#include "file.cpp"


typedef long double LD;
typedef map<char, pair<LD, LD>> ttable;
using namespace std;
class Coder {
  public:
    LD l;
    string text;
    string output;
    ttable pTable;

    Coder(LD length, string inputText, string action, ttable table = {}) {
      pTable = table;
      l = length;
      cout << "L: " << l << endl;
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
      map<char, LD> table;
      for (auto c : text) {
        table[c]++; 
      }

      LD last = 0;
      for (auto i : table) {
        table[i.first] /= (LD)l;
        table[i.first] += last;
        LD temp = table[i.first];
        pair<LD, LD> p(last, temp);
        pTable[i.first] = p;
        last = temp;
      }
    }

    LD newPoint(LD s, LD e, LD p) {
      LD r = (e - s) * p + s;
      return r;
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
     LD start = 0, end = 1;
     int i = 0;
     string outputs = "";
     for (auto c : text) {
       pair<LD, LD> ranges(pTable[c]);
       cout << ranges.first << " " << ranges.second << endl;
       LD start1 = newPoint(start, end, ranges.first);
       LD end1 = newPoint(start, end, ranges.second);
       cout << start1 << " " << end1 << endl;
       tuple<LD, LD, string> t(
           enNormalize(start1, end1)
       );
       start = get<0>(t);
       end = get<1>(t);
       outputs += get<2>(t);
     }

     LD result = ((end - start) / (LD)2) + start;
     return outputs + float2bin(result);
   }
   
   string decode(
       string encodedString, 
       map<char, pair<LD, LD>> table
   ) {
     string fullEncoded = encodedString;
     pair<int, int> encodedIdx(0, 400);
     string encodedNumber = "0." + encodedString.substr(
         encodedIdx.first, encodedIdx.second);
     LD encoded = bin2float(encodedNumber);
     LD start, end;
     start = 0;
     end = 1;
     int i = 0;
     string decoded = "";
     while (i < l) {
       for (auto item : table) {
         LD s, e;
         s = item.second.first;
         e = item.second.second;
         LD bigger = newPoint(start, end, s);
         LD smaller = newPoint(start, end, e);
         if (encoded >= bigger && encoded < smaller) {
           decoded += item.first;
           cout << "I : " << i << endl;
           LD start1, end1;
           start1 = newPoint(start, end, s);
           end1 = newPoint(start, end, e);
           tuple<LD, LD, LD, pair<int, int>> t;
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
     cout << "I : " << i << endl;
     return decoded;
   }

   tuple<LD, LD, LD, pair<int, int>> deNormalize(
       LD initStart, 
       LD initEnd, 
       LD initNumber, 
       string fullNumber, 
       pair<int, int> numberIndex
       ) {
     string start, end, number;
     start = float2bin(initStart);
     end = float2bin(initEnd);
     number = float2bin(initNumber);
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
       number = get<0>(leftShift(number, amount, "end", fullNumber, numberIndex));

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


   tuple<LD, LD, string> enNormalize(LD initStart, LD initEnd) {
     string start, end;
     start = float2bin(initStart);
     end = float2bin(initEnd);
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
  string text =  "hello I am your fat";
  cout << text << " " << text.length();
  Coder en(text.length(), text, "encode");
  string out = en.output;
  cout << "output: " << out << endl;
  File file("test");
  file.write(en.pTable, en.output, (int)en.l);
  tuple<ttable, string, int> data = file.read();

  //Coder de(get<2>(data), get<1>(data), "decode", get<0>(data));
  Coder de(text.length(), en.output, "decode", en.pTable);
  cout << "output: " << de.output << " " << de.output.length() << endl;
}

