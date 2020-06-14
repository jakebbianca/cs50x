// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
// 33 is the constant from the djb2 hash fucntion
const unsigned int N = 256;

// count of words for dictionary size
unsigned int dictsize = 0;


// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    unsigned int index = hash(word);
    while (index >= N)
    {
        index = index % 10;
    }

    if (table[index] == NULL)
    {
        return false;
    }

    node *cursor = table[index];

    if (cursor == NULL)
    {
        return false;
    }

    if (strcasecmp(word, cursor->word) == 0)
    {
        return true;
    }

    while (cursor->next != NULL)
    {
        cursor = cursor->next;

        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
//Hash function "djb2" created by Dan Bernstein, found at http://www.cse.yorku.ca/~oz/hash.html
unsigned long hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c); /* hash * 33 + c */
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Failed to load dictionary file.\n");
        return false;
    }

    //Allocate memory for the word, then fill with 0 and NUL (essentially calloc)
    char *word = malloc(sizeof(char[LENGTH + 1]));

    if (word == NULL)
    {
        printf("Failed to allocate memory for char *word.\n");
    }

    unsigned int wordcount = 0;
    //read strings from file
    while (fscanf(dict, "%s", word) != EOF)
    {
        if (word == NULL)
        {
            printf("Failed to read from dictionary file.\n");
            return false;
        }

        word[LENGTH] = '\0';

        //Keep count of words in dictionary
        wordcount++;

        //create a new node
        //do i need to have a node pointer name in this loop that changes each loop?
        node *n = malloc(sizeof(node));
        strcpy(n->word, word);
        n->next = NULL;

        //hash the word
        unsigned int index = hash(word);

        while (index >= N)
        {
            index = index % 10;
        }

        if (table[index] == NULL)
        {
            table[index] = n;
        }
        else
        {
            n->next = table[index]->next;
            table[index]->next = n;
        }


    }
    fclose(dict);
    dictsize = wordcount;
    free(word);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dictsize;
}

// Unloads dictionary from memory, returning true if successful else false
//Can iterate through all of the linked lists in the hash table and free one by one
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            return true;
        }

        node *cursor = table[i];
        node *tmp = cursor;

        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }

        free(tmp);
    }

    return true;

    return false;
    printf("Unload function failed.");
}
