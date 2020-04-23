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
        exit(1);
        return 1;
    }
    //if the length of the command line argument string is NOT 26 characters, print error...
    if (strlen(key) != 26)
    {
        printf("Error: Input key length must be exactly 26 characters.\n");
        exit(1);
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
            exit(1);
            return 1;
        }
    }
    //if argv[1] contains any duplicate alphabetical characters...
    for (int i = 0; key[i] != '\0'; i++)
    {
        int j = i + 1;
        while (key[j] != '\0')
        {
            if (key[i] == key[j])
            {
                printf("Error: Input key must not contain any duplicate letters.\n");
                exit(1);
                return 1;
            }
            j++;
        }
    }
    string pt = get_string("plaintext: ");
    int ptlen = strlen(pt);
    printf("ciphertext ");
    for (int i = 0; i < ptlen; i++)
    {
        if (islower(pt[i]) != 0)
        {
            int map = pt[i] - 97;
            printf("%c", tolower(key[map]));
        }
        else if (isupper(pt[i]) != 0)
        {
            int map = pt[i] - 65;
            printf("%c", toupper(key[map]));
        }
        else
        {
            printf("%c", pt[i]);
        }
    }
    printf("\n");
    return 0;
}