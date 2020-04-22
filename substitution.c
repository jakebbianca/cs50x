//Library declarations
#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
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
    //Ask user for plaintext input
    string pt = get_string("plaintext: ");
    string ct = pt;
    //Conversion of plaintext to cyphertext
    for (int i = 0; pt[i] != '\0'; i++)
    {
        int pt0 = pt[i];
        int ptplus3 = (int) pt[i] + 3;
        int ptminus23 = (int) pt[i] - 23;
        //if a given letter's ASCII decimal value + 3 does not go past bound of z, regardless of case, modify the ct letter int value by + 3
        if ((pt0 >= 65 && pt0 <= 90 && ptplus3 >= 65 && ptplus3 <= 90) || (pt0 >= 97 && pt0 <= 122 && ptplus3 >= 97 && ptplus3 <= 122))
        {
            ct[i] = (char) ptplus3;
        }
        else if ((pt0 >= 65 && pt0 <= 90 && ptplus3 > 90) || (pt0 >= 97 && pt0 <= 122 && ptplus3 > 122))
        {
            ct[i] = (char) ptminus23;
        }
    }
    //Print output, maintaining letter case if character is alphabetical
    printf("cyphertext: %s", ct);
    printf("\n");
}