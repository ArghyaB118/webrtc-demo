#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>

using namespace std;

// https://stackoverflow.com/questions/29058452/how-to-convert-a-bmp-image-into-byte-array-using-c-program

# define BYTES_PER_PIXEL 4
# define BITMAP_HEADER 54
uint8_t k = 0;

int main() {
  for (int i = 0; i < 171; i++) {
    printf("reading %d-th image", i);
    string command = "./test-ffmpeg-frame-extractor.sh " + to_string(i);
    system(command.c_str());
    FILE *fp = fopen("frames/out.bmp", "rb");
    fseek(fp, 0, SEEK_SET);
    fseek(fp, BITMAP_HEADER, SEEK_SET);
  
    for (int i = 0; i < 1920; i++)
      for (int j = 0; j < 1080*BYTES_PER_PIXEL; j++)
        int bytes = fread(&k, 1, 1, fp);
  
    fclose(fp); 
  }
  return 0;
}


