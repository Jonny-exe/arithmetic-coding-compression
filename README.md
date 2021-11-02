# arithmetic-coding-compression

This is an implementation (written in python) of arithmetic coding for compression.

Note: this is not made for serious use

The results of this encoder are:

```
enwik4: 10k  -->  7k
enwik5: 100k --> 63k
```

Arguments for encoder:

```
JZIP

optional arguments:
  -h, --help  show this help message and exit
  -d D        decode
  -e E        encode
```

TODO:
  - Make it so you can compress folders
  - Make it work with files not encoded in utf-8
  - Make it for images
  - Write in C++

	
