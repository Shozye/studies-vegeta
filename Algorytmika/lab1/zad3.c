#include<stdio.h>

int length(char* word){
    int len = 0;
    while (*word != 0){len++; word++;}
    return len;
}

int min(int a, int b){ if(a < b) return a; return b;}

int is_suffix2(char* code, int n, char* word, int m){
    for(int i = 0; i < n; i++){
        if (word[m-n + i] != code[i]) return 0;
    }    
    return 1;
}


int get_prefix_suffix2(char* w1, int n, char* w2, int m){
    int k = min(n, m);
    while(!is_suffix2(w1, k, w2, m) && k != 0){
        k--;
    }
    return k;

}
int get_prefix_suffix(char* w1, char* w2){
    return get_prefix_suffix2(w1, length(w1), w2, length(w2));
}

int main(){
    if(get_prefix_suffix("rzysztof", "patrzy") != 3){ printf("Error 1\n");}
    if(get_prefix_suffix("janoqfn", "asccspogerja") != 2){ printf("Error 2\n");}
}