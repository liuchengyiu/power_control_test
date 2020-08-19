#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
int main() {
    int fd;
    unsigned char cmd = 0;
    unsigned char cmd1 = 0;
    fd = open("/dev/ledctrl", O_RDWR);
    if (fd < 0) {
        printf("device cant open \n");
        return -1;
    }
    write(fd, &cmd, sizeof(cmd));
    close(fd);
    fd = open("/dev/ledwan", O_RDWR);
    if (fd < 0) {
        printf("device cant open \n");
        return -1;
    }
    write(fd, &cmd1, sizeof(cmd1));
    close(fd);
    return 0;
}