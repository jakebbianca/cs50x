//Conditions and relational operators

#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Prompt user for answer
    string answer = get_string("What is your name?\n");

    //Respond to user input for answer
    printf("hello, %s\n", answer);
}
