#include<stdio.h>
#include<string.h>

int min(int a, int b){ if(a < b) return a; return b;}

int length(char* word){
    int len = 0;
    while (*word != 0){len++; word++;}
    return len;
}

void match2(char* code, int n, char* word, int m){
    for(int i = 0; i < m-n+1; i++){
        if(memcmp(code, word+i,n) == 0){
            printf("found:%d\n", i);
        }
    }
}

void match(char* code, char* word){
    match2(code, length(code), word, length(word));
}

int main(){
    match("ana", "analfabetanakondana");
}