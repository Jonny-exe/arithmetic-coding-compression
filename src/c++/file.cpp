#include<bits/stdc++.h>
#include "modules/json.hpp"

using json = nlohmann::json;
typedef map<char, pair<double, double>> ttable;
class File  {
  public:
    string filename;
    string HEADER = "JZIP";
    int VERSION = 2;

    File(string f) {
      filename = f;
    }

    int write(ttable table, string encoded, int l) {

      ofstream file;
      file.open(filename + ".jzip", ios::binary);

      file << HEADER;
      file << VERSION;

      json jt = table;
      string js = jt.dump();
      file << js.length(); //TODO: make sure this is written in binary and not in ascii
      file << ";";
      file << js;
      file << l;
      for (int i = 0; i < encoded.length() % 8; i++) {
        encoded = "0" + encoded;
      }

      int idx = 0;
      string block;
      // You can't do all at once because of overflow
      for (int i = 0; i < encoded.length(); i++) {
        if (i % 8 == 0 && i != 0) {
          file << stoi(block, nullptr, 2);
          block = "";
          continue;
        }
        block += encoded[i];
      }
      return 0;
    }

    tuple<ttable, string> read() {

      ifstream file;
      file.open(filename + ".jzip", ios::binary);
      unsigned char ch;

      int p = 4;

      char name[p];
      file.get(name, p);
      string nameStr = str(name);
      if (name != "JZIP") throw runtime_error("Header not valid");
      
      p++;
      unsigned char version = file.get();
      if (version != 2) throw runtime_error("Version not valid");

      int tablel = 0;
      unsigned char i;
      while (i = file.get()) {
        p++;
        if (i == ';') {
          break;
        }
        tablel += (int)i;
      }

      char str[tablel];
      file.get(str, tablel + p);
      json jt = json.parse(str);
      ttable table = jt.get<ttable>;
      unsigned char encodedCh[file.tellg()];
      file.get(encodedCh, file.tellg());

      string encoded = str(encodedCh);
      return make_tuple(table, encoded);
    }
};
