#include<stdio.h>
#include<string.h>

unsigned long djb2(char *str, int s, int n)
{
    unsigned long hash = 0;
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

unsigned long powmy(unsigned long a, unsigned long p){
    unsigned long ans = 1;
    for(int i = 0; i < p; i++){
        ans *= a;
    }
    return ans;
}


void matchRabinKarp(char* pattern, char* text){
    int patternLen =  length(pattern);
    int textLen = length(text);

    unsigned long hashed_pattern = djb2(pattern, 0, patternLen);
    unsigned long hash = djb2(text, 0, patternLen);
    if (hash == hashed_pattern){
        printf("%d\n", 0);
    }
    unsigned long mult = powmy(33, patternLen-1);
    for(int i = 1; i < textLen - patternLen + 1; i++){
        
        hash = hash - text[i-1] * mult;
        hash = ((hash << 5) + hash) + text[i + patternLen - 1]; 
        if (hash == hashed_pattern){
            printf("Checking... %d\n", i);

            int good = 1;
            for(int j = 0; j < patternLen; j++){
                if (pattern[j] != text[i+j]){
                    good = 0;
                }
            }
            if (good){
                printf("OK!\n");
            }
        }
    }

}

int main(){
    
    matchRabinKarp("ana", "analfabetanakondana");
}


