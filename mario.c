//Conditions amnd relational operators

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // define integer h, i and j
    int h, i, j;
    // ask for 'Height' as long as value is < 1 or > 8
    do
    {
        h = get_int("Height: ");
    }
    //Repeat question until h value given is integer from 1 through 8
    while (h < 1 || h > 8);
    //Loop nested loops h times
    for (i = 0; i < h; i++)
    {
        //Loop to print leading spaces, with one less leading space each row as i counts up
        for (j = 0; j < h - i - 1; j++)
        {
            printf(" ");
        }
        //Loop to print 1st pyramid hashes; do I need diff var?
        for (j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        //Print two gap spaces per each outer loop, so per row
        printf("  ");
        //Loop to print second pyramid hashes
        for (j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        //Print new line
        printf("\n");
    }
}
