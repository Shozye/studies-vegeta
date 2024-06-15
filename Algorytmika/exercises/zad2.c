#include<stdio.h>

int is_prefix2(char* code, int n, char* word, int m){
    for(int i = 0; i < n;i++){
        if (word[i] != code[i]) return 0;
    }
    return 1;
}

int is_suffix2(char* code, int n, char* word, int m){
    for(int i = 0; i < n; i++){
        if (word[m-n + i] != code[i]) return 0;
    }    
    return 1;
}

int length(char* word){
    int len = 0;
    while (*word != 0){len++; word++;}
    return len;
}

int is_prefix(char* code, char* word){
    return is_prefix2(code, length(code), word, length(word));
}

int is_suffix(char* code, char* word){
    return is_suffix2(code, length(code), word, length(word));
}

int main(){
    if(!is_prefix("dr. ", "dr. inż Stanisław Michalak"))
        printf("Error PASS is_prefix\n");

    if(is_prefix("dr. ", "dramat"))
        printf("Error FAIL is_prefix\n");
    
    if(!is_suffix(".png", "pack.png"))
        printf("Error PASS is_suffix\n");
    
    if(is_suffix(".png", "png.pngie"))
        printf("Error FAIL is_suffix\n");
}