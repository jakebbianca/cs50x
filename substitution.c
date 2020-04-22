//Library declarations
#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
//argc meaning "argument count", argv[] meaning "argument vector"
//basically, count of arguments including the program ./ and the actual strings input on the command line from the user (hence the array of strings)
int main(int argc, string argv[])
{
    //create string "key" and set as the command line argument after running ./program
    string key = argv[1];
    //if there is <> 1 command line argument, print error message and return a value of 1 (and exit)
    if (argc != 2)
    {
        printf("Error: User must provide exactly one command line argument.\n");
        exit(0);
        return 1;
    }
    //if the length of the command line argument string is NOT 26 characters, print error...
    if (strlen(key) != 26)
    {
        printf("Error: Input key length must be exactly 26 characters.\n");
        exit(0);
        return 1;
    }
    //if agrv[1] does not exclusively alphabetical characters...
    for (int i = 0; key[i] != '\0'; i++)
    {
        char letter0 = key[i];
        int ascii0 = (int) letter0;
        if ((int) letter0 < 65 || ((int) letter0 > 90 && (int) letter0 < 97) || (int) letter0 > 122)
        {
            printf("Error: Input key must contain only alphabetical characters.\n");
            exit(0);
            return 1;
        }
    }
    //if argv[1] contains any duplicate alphabetical characters...
    for (int i = 1; key[i] != '\0'; i++)
    {
        char letter0 = key[0];
        char letter1 = key[i];
        int ascii0 = (int) letter0;
        int ascii1 = (int) letter1;
        if (ascii0 == ascii1 || ascii0 == ascii1 - 32 || ascii0 == ascii1 + 32)
        {
            printf("Error: Input key must not contain any duplicate letters.\n");
            exit(0);
            return 1;
        }
    }
    //Ask user for plaintext to transform
    string pt = get_string("plaintext: ");
    //Create base alphabet string and find conversions from key
    string upperabc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string lowerabc = "abcdefghijklmnopqrstuvwxyz";
    //Print "ciphertext " ahead of decoded printf's
    printf("ciphertext: ");
    for (int i = 0; (int) key[i] != '\0'; i++)
    {
        if (islower(key[i]) != 0)
        {
            printf("%c", lowerabc[i]);
        }
        else if (isupper(key[i]) != 0)
        {
            printf("%c", upperabc[i]);
        }
        else
        {
            printf("Unknown error occurred while deciphering user plaintext.");
            exit(0);
            return 1;
        }
    }
}