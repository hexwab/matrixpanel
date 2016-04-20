#include <math.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/time.h>

uint32_t color_plasma(float val) {
  float unused;
  float r,g,b;
  val = modff(val+1e4, &unused) * 3.0;
  if (val < 1.0) {
    r = val;
    g = 1.0 - r;
    b = 0.0;
  }
  else if (val < 2.0) {
    b = val - 1.0;
    r = 1.0 - b;
    g = 0.0;
  } else {
    g = val - 2.0;
    b = 1.0 - g;
    r = 0.0;
  }
  uint8_t rr = r * 256.0 - 0.5;
  uint8_t gg = g * 256.0 - 0.5;
  uint8_t bb = b * 256.0 - 0.5;
  return rr | (gg << 8) | (bb << 16);
}

#define SZ 64

uint32_t buf[SZ*SZ];
float offset = 0;

#define C1 1
#define C2 0.83
#define C3 0.5
#define C4 0.82
#define C5 10
#define C6 0.5
#define C7 10

void draw(void) {
  float cx1 = 0.5*sinf(offset*C1);
  float cy1 = 0.5*sinf(offset*C2);
  float step = 1.0/SZ;
  float p, q;
  int x,y;
  uint32_t *ptr = buf;
  for (x=0, p=-.5; x<SZ; x++, p+=step) {
    for (y=0, q=-.5; y<SZ; y++, q+=step) {
            float v = sinf(C5*(p*sinf(offset*C3)+q*cosf(offset*C4))+offset);
	    float cx = cx1 + p;
            float cy = cy1 + q;
            v += sinf(C7*sqrt(cx*cx+cy*cy+C6)+offset);
            uint32_t color = color_plasma(v);
	    *ptr++ = color;
    }
  }
  offset += 1./50;
}

int main(void) {
  struct timeval t1, t2;
  gettimeofday(&t1, NULL);
  offset = t1.tv_usec/10000.0;
  int y,z;
  while (1) {
    draw();
    for (y=0; y<64; y++) {
      z = ((y&7) << 3) + (y>>3);
      fwrite(buf+z*SZ,SZ,4,stdout);
    }
    gettimeofday(&t2, NULL);
    if (t2.tv_sec - t1.tv_sec > 30)
      break;
  }
}
