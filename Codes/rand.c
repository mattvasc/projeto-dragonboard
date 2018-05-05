#include<stdio.h>
#include <time.h>
#include <stdlib.h>

int main(){

srand(time(NULL));

printf("%d\n", rand() % 30);

printf("%d", rand() % 1025);

return 0;

}
