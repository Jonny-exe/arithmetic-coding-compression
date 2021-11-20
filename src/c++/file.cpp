#include<bits/stdc++.h>
#include "modules/json.hpp"

using json = nlohmann::json;
typedef map<char, pair<double, double>> ttable;


class File  {
  public:
    struct Header {
      char type[5];
      int version;
      int tablel;
      int encodedl;
      int decodedl;
    };

    string filename;
    char TYPE[5] = "JZIP";
    int VERSION = 2;
    int HEADER_SIZE = 24;

    File(string f) {
      filename = f;
    }

    int write(ttable table, string encoded, int l) {

      ofstream file;
      file.open(filename + ".jzip", ios::binary);

      json jt = table;
      string js = jt.dump();
      int jl = js.length();

      Header header;
      header.version = VERSION;
      strcpy(header.type, TYPE);
      header.tablel = jl;
      header.encodedl = (encoded.length() + (encoded.length() % 8)) / 8;
      header.decodedl = l;

      file.write((char*)&header, sizeof(header));

      //TODO: make sure this is written in binary and not in ascii;
      file << js;
      for (int i = 0; i < encoded.length() % 8; i++) {
        encoded += "0";
      }

      int idx = 0;
      string block;
      // You can't do all at once because of overflow
      for (int i = 0; i < encoded.length(); i++) {
        if (i % 8 == 0 && i != 0) {
          unsigned char a = 0;
          for (int n = 0; n < 8; n++) 
            if (block[n] == '1') a += pow(2, 8 - n - 1);
          file.write((char*)&a, 1);
          block = "";
        }
        block += encoded[i];
      }
      return 0;
    }

    tuple<ttable, string, int> read() {

      ifstream file;
      file.open(filename + ".jzip", ios::binary);
      int p = 0;

      Header header;
      file.read((char*)&header, HEADER_SIZE);

      if (strcmp(header.type, TYPE)) throw runtime_error("Header not valid");
      if (header.version != 2) throw runtime_error("Version not valid"); 

      char jChars[header.tablel];
      file.get(jChars, header.tablel + 1);
      string jString(jChars);
      json jt = json::parse(jString);
      ttable pTable = jt.get<ttable>();

      unsigned char encodedCh[header.encodedl];
      file.get((char*)encodedCh, header.encodedl);

      string encoded;
      for (int i = 0; i < header.encodedl; i++) {
        encoded += std::bitset<8>((int)encodedCh[i]).to_string();
      }
      return make_tuple(pTable, encoded, header.decodedl);
    }
};
