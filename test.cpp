#include <iostream>
#include <vector>
#include <fstream>
using namespace std;

// http://www.ffmpeg.org/doxygen/trunk/api-example_8c-source.html
static void pgm_save(unsigned char *buf, int wrap, int xsize, int ysize, char *filename) {
     FILE *f;
     int i;
 
     f=fopen(filename,"w");
     fprintf(f,"P5\n%d %d\n%d\n",xsize,ysize,255);
     for(i=0;i<ysize;i++)
         fwrite(buf + i * wrap,1,xsize,f);
     fclose(f);
}


// https://gist.github.com/drautb/5571192




static std::vector<char> ReadAllBytes(char const* filename)
{
    ifstream ifs(filename, ios::binary|ios::ate);
    ifstream::pos_type pos = ifs.tellg();

    std::vector<char>  result(pos);

    ifs.seekg(0, ios::beg);
    ifs.read(&result[0], pos);


	int size = 0;
	while (result[size]	!= '\0') size++;
	cout << size << endl;


    return result;
}

int main() {
	vector<char> v = ReadAllBytes("output.mkv");
	return 0;
}


