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
      int jl = js.length();

      file.write( reinterpret_cast<const char *>(&jl), sizeof(jl));
      //TODO: make sure this is written in binary and not in ascii;
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
      file.get(name, p + 1);
      string nameStr = name;
      cout << "name: " << name << strcmp(name, "JZIP") << endl;
      if (strcmp(name, "JZIP")) throw runtime_error("Header not valid");
      
      p++;
      char version = file.get();

      cout << "version: " << version << endl;
      if (version == 2) throw runtime_error("Version not valid"); 
      unsigned char * chars;
      chars = new unsigned char[4];
      file.read((char*)chars, 4);

      int tablel = (int)chars[0] + ((int)chars[1] << 8) + ((int)chars[2] << 16) + ((int)chars[3] << 24);

      cout << "tablel: " << tablel << endl;
      char charArr[tablel];
      file.get(charArr, tablel + p + 1);
      string str(charArr);
      json jt = json::parse(str);
      ttable table = jt.get<ttable>();
      unsigned char encodedCh[(long int)file.tellg()];
      string encoded(encodedCh,  encodedCh + sizeof encodedCh / sizeof encodedCh[0]);

      return make_tuple(table, encoded);
    }
};
