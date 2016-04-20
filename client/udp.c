/* 
 * udpclient.c - A simple UDP client
 * usage: udpclient <host> <port>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define BUFSIZE 520

/* 
 * error - wrapper for perror
 */
void error(char *msg) {
  perror(msg);
  exit(0);
}

int main(int argc, char **argv) {
  int sockfd, portno, n;
  int serverlen;
  struct sockaddr_in serveraddr;
  struct hostent *server;
  char *hostname;
  struct {
    unsigned char magic;
    unsigned char n2;
    unsigned char n1;
    unsigned char padding[5];
    char buf[512];
  } pkt;

  int i;
  
  /* check command line arguments */
  if (argc != 3) {
    fprintf(stderr,"usage: %s <hostname> <port>\n", argv[0]);
    exit(0);
  }
  hostname = argv[1];
  portno = atoi(argv[2]);

  /* socket: create the socket */
  sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0)
    error("ERROR opening socket");

  /* gethostbyname: get the server's DNS entry */
  server = gethostbyname(hostname);
  if (server == NULL) {
    fprintf(stderr,"ERROR, no such host as %s\n", hostname);
    exit(0);
  }

  /* build the server's Internet address */
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  bcopy((char *)server->h_addr,
	(char *)&serveraddr.sin_addr.s_addr, server->h_length);
  serveraddr.sin_port = htons(portno);
  
  pkt.n1 = pkt.n2 = 0;
  memset(pkt.padding, 0, sizeof(pkt.padding));
  while (1) {
    if (fread(pkt.buf, 512, 1, stdin) <= 0)
      exit(1);
      pkt.magic = 3;
      /* send the message to the server */
      n = sendto(sockfd, &pkt, sizeof(pkt), 0, &serveraddr, sizeof(serveraddr));
      usleep(350);
      if (n < 0)
	error("ERROR in sendto");
      if (++pkt.n1 == 32) {
	pkt.n1 = 0;
	pkt.magic = 1;
	n = sendto(sockfd, &pkt, 4, 0, &serveraddr, sizeof(serveraddr));
	usleep(4000);
	pkt.n2++;
      }
  }
    
  return 0;
}
