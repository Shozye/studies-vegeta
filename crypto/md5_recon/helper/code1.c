#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mbedtls/md5.h"

// Oryginalne wartości IV
unsigned char IV[16] = {
    0x01, 0x23, 0x45, 0x67,
    0x89, 0xab, 0xcd, 0xef,
    0xfe, 0xdc, 0xba, 0x98,
    0x76, 0x54, 0x32, 0x10
};

unsigned char M0[64];
unsigned char M1[64];
unsigned char M0_prime[64];
unsigned char M1_prime[64];


unsigned char hex_to_unsigned_char(const char *hex) {
    unsigned char value;
    sscanf(hex, "%2hhx", &value);  // Przekształca dwa znaki szesnastkowe na jeden unsigned char
    return value;
}

void process_message(char *message, unsigned char *output, int *output_index, int little_endian) {
    char *token;
    char processed_message[1000] = "";  // Przechowuje przetworzony ciąg
    char block[9]; // Dla bloków o długości 8 znaków

    // Dzielimy wiadomość na bloki według spacji
    token = strtok(message, " ");
    while (token != NULL) {
        // Sprawdzenie długości bloku
        if (strlen(token) == 7) {
            // Jeśli blok ma 7 znaków, dodajemy '0' na początku
            char corrected_block[9] = "0";
            strcat(corrected_block, token);
            strcpy(block, corrected_block);  // Użyjemy poprawionego bloku
        } else {
            strcpy(block, token);  // Używamy oryginalnego bloku
        }

        // Przekształcenie bloków w unsigned char
        for (int i = 0; i < 8; i += 2) {
            output[*output_index] = hex_to_unsigned_char(&block[i]);  // Przekształcamy dwa znaki w unsigned char
            (*output_index)++;
        }
        
        token = strtok(NULL, " ");  // Przechodzimy do kolejnego bloku
    }

    // Jeżeli flaga little_endian jest ustawiona
    if (little_endian) {
        unsigned char temp[64] = {0};  // Tablica tymczasowa do przechowywania przekształconych bajtów
        int temp_index = 0;

        // Odwracamy kolejność bajtów w blokach po 4 bajty
        for (int i = 0; i < *output_index; i += 4) {
            if (i + 3 < *output_index) {  // Sprawdzamy, czy mamy pełne 4 bajty
                temp[temp_index++] = output[i + 3];
                temp[temp_index++] = output[i + 2];
                temp[temp_index++] = output[i + 1];
                temp[temp_index++] = output[i];
            }
        }
        memcpy(output, temp, temp_index);  // Kopiujemy przekształcone bajty z powrotem do output
        *output_index = temp_index;  // Uaktualniamy liczbę bajtów
    }
}

void read_file(const char* filename, int little_endian) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Unable to open file: %s\n", filename);
        return;
    }

    // Tablice na dwie wiadomości
    char messageM0[1000];
    char messageM1[1000];
    char messageM0prime[1000];
    char messageM1prime[1000];

    // Odczyt dwóch linii z pliku
    fgets(messageM0, sizeof(messageM0), file);
    fgets(messageM1, sizeof(messageM1), file);
    fgets(messageM0prime, sizeof(messageM0prime), file);
    fgets(messageM1prime, sizeof(messageM1prime), file);

    // Usunięcie ewentualnych nowych linii na końcu
    messageM0[strcspn(messageM0, "\n")] = 0;
    messageM1[strcspn(messageM1, "\n")] = 0;
    messageM0prime[strcspn(messageM0prime, "\n")] = 0;
    messageM1prime[strcspn(messageM1prime, "\n")] = 0;

    fclose(file);

    // Tablica na wynikowe unsigned char
    unsigned char outputM0[64] = {0};
    unsigned char outputM1[64] = {0};
    unsigned char outputM0prime[64] = {0};
    unsigned char outputM1prime[64] = {0};
    int M0index = 0;
    int M1index = 0;
    int M0primeindex = 0;
    int M1primeindex = 0;
    
    // Przetwarzanie wiadomości
    printf("Original Message M0: %s\n", messageM0);
    process_message(messageM0, outputM0, &M0index, little_endian);
    memcpy(M0, outputM0, 64);

    printf("Original Message M1: %s\n", messageM1);
    process_message(messageM1, outputM1, &M1index, little_endian);
    memcpy(M1, outputM1, 64);

    printf("Original Message M0_prime: %s\n", messageM0prime);
    process_message(messageM0prime, outputM0prime, &M0primeindex, little_endian);
    memcpy(M0_prime, outputM0prime, 64);

    printf("Original Message M1_prime: %s\n", messageM1prime);
    process_message(messageM1prime, outputM1prime, &M1primeindex, little_endian);
    memcpy(M1_prime, outputM1prime, 64);

//     // Wyświetlanie wyników
//     printf("Output 1: ");
//     for (int i = 0; i < M0index; i++) {
//         printf("0x%02x ", outputM0[i]);
//     }
//     printf("\n");

//     printf("Output 2: ");
//     for (int i = 0; i < M1index; i++) {
//         printf("0x%02x ", outputM1[i]);
//     }
//     printf("\n");
 }

void print_hash(unsigned char hash[16]) {
    for (int i = 0; i < 16; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

void print_m(unsigned char hash[64]) {
    for (int i = 0; i < 64; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

// Funkcja do obliczania MD5
void calculate_md5(unsigned char *input, size_t input_len, unsigned char *output) {
    mbedtls_md5_context ctx;
    mbedtls_md5_init(&ctx);
    mbedtls_md5_starts(&ctx);
    mbedtls_md5_update(&ctx, input, input_len);
    mbedtls_md5_finish(&ctx, output);
}

// Funkcja do obliczania podwójnego MD5
void double_md5(unsigned char *iv, unsigned char *M0, size_t M0_len, unsigned char *M1, size_t M1_len, unsigned char *output) {
    unsigned char temp_hash[16];

    // Oblicz MD5 dla M0 + M1
    unsigned char *combined_M0 = malloc(M0_len + M0_len); // 16 (IV) + M0_len
    memcpy(combined_M0, M0, M0_len);
    memcpy(combined_M0 + M0_len, M1, M1_len);
    
    // calculate_md5(combined_M0, 16 + M0_len, temp_hash);
    // free(combined_M0); // Zwolnienie pamięci

    // // Oblicz MD5 dla (MD5(IV, M0) + M1)
    // unsigned char *combined_final = malloc(16 + M1_len); // 16 (temp_hash) + M1_len
    // memcpy(combined_final, temp_hash, 16);
    // memcpy(combined_final + 16, M1, M1_len);

    calculate_md5(combined_M0, M0_len + M1_len, output);
    free(combined_M0); // Zwolnienie pamięci
}

int main(int argc, char *argv[]) {

    if (argc < 3) {
        printf("za malo argumentow: 1-nazwa pliku, 2-czy kodowac w little idniana\n", argv[0]);
        return 1;
    }

    read_file(argv[1], argv[2]);
    

    unsigned char hash1[16], hash2[16];

    // Obliczanie MD5 dla (IV + M0) + M1
    double_md5(IV, M0, sizeof(M0), M1, sizeof(M1), hash1);
    
    // Obliczanie MD5 dla (IV + M0') + M1'
    double_md5(IV, M0_prime, sizeof(M0_prime), M1_prime, sizeof(M1_prime), hash2);

    // Wyświetl wyniki
    printf("Hash 1: ");
    print_hash(hash1);
    printf("Hash 2: ");
    print_hash(hash2);

    // Porównanie hashy
    if (memcmp(hash1, hash2, 16) == 0) {
        printf("Kolizja znaleziona!\n");
    } else {
        printf("Brak kolizji.\n");
    }

    printf("\n");
    print_m(M1);

    return 0;
}