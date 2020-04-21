//libraries
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
//call nested functions
int count_letters(string s0);
int count_words(string s0);
int count_sentences(string s0);
//main function
int main(void)
{
    //Create character array s, get user input to determine value
    string s = get_string("Text: ");
    int letter_count = count_letters(s);
    int word_count = count_words(s);
    int sentence_count = count_sentences(s);
    //L is the variable for average count of words per 100 letters
    float L = (100 * (float)letter_count / ((float)word_count));
    //S is the variable for average count of sentences per 100 words
    float S = (100 * (float)sentence_count / (float)word_count);
    //Coleman-Liau index = 0.0588 * L - 0.296 * S - 15.8
    float rawindex = (0.0588 * L) - (0.296 * S) - 15.8;
    //round to the nearest grade value
    int index = round(rawindex);
    //loop to print correct value
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

//nested functions

int count_letters(string s0)
{
    int count0 = 0;
    for (int i = 0; s0[i] != '\0'; i++)
    {
        if (isalpha(s0[i]) != 0)
        {
            count0++;
        }
    }
    return count0;
}

int count_words(string s1)
{
    int count1 = 1;
    for (int i = 0; s1[i] != '\0'; i++)
    {
        if (isspace(s1[i]) != 0)
        {
            count1++;
        }
    }
    return count1;
}
//36,43.63 == !,.,?
int count_sentences(string s2)
{
    int count2 = 0;
    for (int i = 0; s2[i] != '\0'; i++)
    {
        if ((s2[i] == '.' || s2[i] == '?' || s2[i] == '!') && ispunct(s2[i + 1]) == 0)
        {
            count2++;
        }
    }
    return count2;
}