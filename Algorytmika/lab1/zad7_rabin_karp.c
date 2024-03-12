#include<stdio.h>

unsigned long djb2(char *str, int s, int n)
{
    unsigned long hash = 5381;
    int c;

    for(int i = s; i < s+n; i++){
        hash = ((hash << 5) + hash) + str[i]; 
    }
    return hash;
}


int length(char* word){
    int len = 0;
    while (*word != 0){len++; word++;}
    return len;
}

void matchRabinKarp(char* pattern, char* text){
    int patternLen =  length(pattern);
    int textLen = length(text);

    unsigned long hashed_pattern = djb2(pattern, 0, patternLen);
    for(int i = 0; i < textLen - patternLen + 1; i++){
        unsigned long hash_current_part = djb2(text, i, patternLen);
        if (hash_current_part == hashed_pattern){
            printf("%d\n", i);
        }
    }

}

int main(){
    
    matchRabinKarp("ana", "analfabetanakondana");
}


