/* Project-authored fixed-work FFTW benchmark. No network or hidden target table. */
#include <fftw3.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define N 8192
#define CLIPS 3
#define REPEATS 256
static uint64_t ns(void){struct timespec t;if(clock_gettime(CLOCK_MONOTONIC,&t))exit(8);return (uint64_t)t.tv_sec*1000000000ULL+t.tv_nsec;}
static void fill(fftw_complex *a,const double *x,int stride){for(int i=0;i<N;i++){a[i*stride][0]=x[i];a[i*stride][1]=0;}}
int main(int argc,char **argv){
 if(argc!=7)return 2;
 int rigor=atoi(argv[1]),threads=atoi(argv[2]),inplace=atoi(argv[3]),stride=atoi(argv[4]);
 if(rigor<0||rigor>2||(threads!=1&&threads!=2&&threads!=4)||(inplace!=0&&inplace!=1)||(stride!=1&&stride!=2))return 2;
 FILE *f=fopen(argv[5],"rb");if(!f)return 3;
 double *x=malloc(sizeof(double)*N*CLIPS);
 if(!x||fread(x,sizeof(double),N*CLIPS,f)!=N*CLIPS||fgetc(f)!=EOF)return 3;fclose(f);
 if(!fftw_init_threads())return 4;
 fftw_plan_with_nthreads(threads);fftw_set_timelimit(.02);
 fftw_complex *a=fftw_malloc(sizeof(fftw_complex)*N*stride),*b=inplace?a:fftw_malloc(sizeof(fftw_complex)*N*stride);
 if(!a||!b)return 5;memset(a,0,sizeof(fftw_complex)*N*stride);
 unsigned flags=rigor==0?FFTW_ESTIMATE:rigor==1?FFTW_MEASURE:FFTW_PATIENT;int n=N;
 uint64_t t=ns();fftw_plan p=fftw_plan_many_dft(1,&n,1,a,NULL,stride,N*stride,b,NULL,stride,N*stride,FFTW_FORWARD,flags);uint64_t planning=ns()-t;
 if(!p)return 6;
 FILE *out=fopen(argv[6],"wb");if(!out)return 7;
 uint64_t times[CLIPS],total=0;
 for(int c=0;c<CLIPS;c++){
  const double *clip=x+c*N;
  for(int k=0;k<8;k++){fill(a,clip,stride);fftw_execute(p);}
  t=ns();for(int k=0;k<REPEATS;k++){fill(a,clip,stride);fftw_execute(p);}times[c]=ns()-t;total+=times[c];
  for(int i=0;i<N;i++)if(fwrite(b[i*stride],sizeof(double),2,out)!=2)return 7;
 }
 if(fclose(out))return 7;
 printf("{\"version\":\"%s\",\"n\":%d,\"clips\":%d,\"iterations_per_clip\":%d,\"warmup_per_clip\":8,\"planning_ns\":%llu,\"target_ns\":%llu,\"workload_ns\":[%llu,%llu,%llu]}\n",fftw_version,N,CLIPS,REPEATS,(unsigned long long)planning,(unsigned long long)total,(unsigned long long)times[0],(unsigned long long)times[1],(unsigned long long)times[2]);
 fftw_destroy_plan(p);if(!inplace)fftw_free(b);fftw_free(a);fftw_cleanup_threads();free(x);return 0;
}
