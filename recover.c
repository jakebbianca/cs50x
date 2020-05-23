#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

//Define the BYTE data type as an unisigned 8-bit integer
typedef uint8_t BYTE;
//Open memory card
//Repeat until end of card:
    //Read 512 bytes into a buffer array
    //If start of a new JPEG
        //If 1st JPEG .. else if new non-1st JPEG
    //Else
        //If already found a jpeg and writing to it, keep writing to it
//Close any remaining files
int main(int argc, char *argv[])
{
    //Program should accept only one command line argument after program execution argument
    if (argc != 2)
    {
        printf("Expecting ./recover [single argument].\n");
        return 1;
    }
    //Open the file given in the command line argument
    FILE *memcard = fopen(argv[1], "r");
    if (memcard == NULL)
    {
        return 2;
        printf("Failed to open file. Null pointer returned.\n");
    }
    //Dynamically allocate the memory for a block-sized array
    //ALWAYS CHECK if malloc pointer == null, don't continue running program if this is the case
    BYTE *pblock_array = malloc(sizeof(BYTE)*512);
    if (pblock_array == NULL)
    {
        printf("Malloc for block array failed.\n");
        return 3;
    }
    //Start reading through the blocks, checking for JPEG headers
    int jpgct = 0;
    //Allocate memory for a string that is enough to include characters "###.jpg" AND the NULL terminating character
    char *jpgname = malloc(sizeof(char)*8);
    FILE *img = NULL;
    while (fread(pblock_array, 1, 512, memcard) == 512)
    {
        //Last syntax -- just look at first four bites of the fourth byte, setting the remaining four bits to 0, thus all 0xe() bytes become 0xe0
        if (pblock_array[0] == 0xff && pblock_array[1] == 0xd8 && pblock_array[2] == 0xff && (pblock_array[3] & 0xf0) == 0xe0)
        {
            //If not first JPEG, close current open file
            if (jpgct > 0)
            {
                fclose(img);
            }
            //Prints name of current JPEG to a string
            sprintf(jpgname, "%03i.jpg", jpgct);
            //Opens file stored at pointer jpgname for writing
            img = fopen(jpgname, "w");
            fwrite(pblock_array, 1, 512, img);

            //Add to JPG count for each new JPG before checking next block of 512 bytes
            jpgct++;
        }
        else if (jpgct > 0)
        {
            fwrite(pblock_array, 1, 512, img);
        }
    }

    if (jpgct == 0)
    {
        free(pblock_array);
        free(jpgname);
        printf("No JPEGs detected.\n");
        return 4;
    }
    //Write data at end of memory card
    fwrite(pblock_array, 1, 512, img);
    //Close last JPEG file and memory card
    fclose(img);
    fclose(memcard);

    //Once finished working with pblock_array, free the memory
    free(pblock_array);
    free(jpgname);
}