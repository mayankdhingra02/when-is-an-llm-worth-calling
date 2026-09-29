/* Local deterministic correctness-checking client, project-authored, no remote mode. */
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#define CLIENTS 4
#define BATCHES 1000
#define PIPELINE 32
#define VALUE_SIZE 1024
static pthread_mutex_t lock=PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cv=PTHREAD_COND_INITIALIZER;
static int ready=0,go=0;
typedef struct {int id,port,failed;long checked;} Job;
static int transfer(int fd,char *buf,size_t n,int sending){size_t at=0;while(at<n){ssize_t k=sending?send(fd,buf+at,n-at,0):recv(fd,buf+at,n-at,0);if(k<=0)return -1;at+=(size_t)k;}return 0;}
static double seconds(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}
static void *worker(void *arg){Job *j=arg;int fd=socket(AF_INET,SOCK_STREAM,0),one=1;struct timeval timeout={5,0};struct sockaddr_in a={0};a.sin_family=AF_INET;a.sin_port=htons(j->port);inet_pton(AF_INET,"127.0.0.1",&a.sin_addr);
 if(fd<0)j->failed=1;else {setsockopt(fd,IPPROTO_TCP,TCP_NODELAY,&one,sizeof(one));setsockopt(fd,SOL_SOCKET,SO_RCVTIMEO,&timeout,sizeof(timeout));setsockopt(fd,SOL_SOCKET,SO_SNDTIMEO,&timeout,sizeof(timeout));if(connect(fd,(void*)&a,sizeof(a)))j->failed=1;}
 char value[VALUE_SIZE];memset(value,'A'+j->id,VALUE_SIZE);
 pthread_mutex_lock(&lock);ready++;pthread_cond_broadcast(&cv);while(!go)pthread_cond_wait(&cv,&lock);pthread_mutex_unlock(&lock);
 for(int b=0;b<BATCHES && !j->failed;b++){char request[65536],expect[65536],received[65536];size_t nr=0,ne=0;
  for(int op=0;op<PIPELINE;op++){int key=(b*16+op/2)%256;
   if(op%2==0){nr+=sprintf(request+nr,"get k%d_%03d\r\n",j->id,key);ne+=sprintf(expect+ne,"VALUE k%d_%03d 0 1024\r\n",j->id,key);memcpy(expect+ne,value,VALUE_SIZE);ne+=VALUE_SIZE;memcpy(expect+ne,"\r\nEND\r\n",7);ne+=7;}
   else {nr+=sprintf(request+nr,"set k%d_%03d 0 0 1024\r\n",j->id,key);memcpy(request+nr,value,VALUE_SIZE);nr+=VALUE_SIZE;memcpy(request+nr,"\r\n",2);nr+=2;memcpy(expect+ne,"STORED\r\n",8);ne+=8;}
  }
  if(transfer(fd,request,nr,1)||transfer(fd,received,ne,0)||memcmp(expect,received,ne))j->failed=1;else j->checked+=PIPELINE;
 }
 if(fd>=0)close(fd);return NULL;
}
int main(int argc,char **argv){if(argc!=2)return 2;int port=atoi(argv[1]);if(port<1024||port>65535)return 2;signal(SIGPIPE,SIG_IGN);pthread_t threads[CLIENTS];Job jobs[CLIENTS];
 for(int i=0;i<CLIENTS;i++){jobs[i]=(Job){i,port,0,0};if(pthread_create(&threads[i],NULL,worker,&jobs[i]))return 3;}
 pthread_mutex_lock(&lock);while(ready<CLIENTS)pthread_cond_wait(&cv,&lock);double start=seconds();go=1;pthread_cond_broadcast(&cv);pthread_mutex_unlock(&lock);
 long count=0;int failures=0;for(int i=0;i<CLIENTS;i++){pthread_join(threads[i],NULL);count+=jobs[i].checked;failures+=jobs[i].failed;}double elapsed=seconds()-start;
 printf("{\"seconds\":%.9f,\"checked_operations\":%ld,\"failed_clients\":%d,\"clients\":4,\"batches_per_client\":1000,\"pipeline\":32}\n",elapsed,count,failures);return failures||count!=128000?2:0;
}
