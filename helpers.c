#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float rgbavg;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            rgbavg = round(((float)image[i][j].rgbtBlue + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtRed) / 3);
            image[i][j].rgbtBlue = rgbavg;
            image[i][j].rgbtGreen = rgbavg;
            image[i][j].rgbtRed = rgbavg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float blu0, blu1, grn0, grn1, red0, red1;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            blu0 = (float)image[i][j].rgbtBlue;
            grn0 = (float)image[i][j].rgbtGreen;
            red0 = (float)image[i][j].rgbtRed;
            blu1 = .272 * red0 + .534 * grn0 + .131 * blu0;
            grn1 = .349 * red0 + .686 * grn0 + .168 * blu0;
            red1 = .393 * red0 + .769 * grn0 + .189 * blu0;
            if (blu1 > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(blu1);
            }
            if (grn1 > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(grn1);
            }
            if (red1 > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(red1);
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmparr[height][width];
    float mirror = ((float)width - 1) / 2;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if ((float)j < mirror || (float)j > mirror)
            {
                tmparr[i][j] = image[i][width - j - 1];
            }
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tmparr[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmparr[height][width];
    float bluavg = 0;
    float grnavg = 0;
    float redavg = 0;
    int iminus, iplus, jminus, jplus;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float n = 0;
            iminus = i - 1;
            iplus = i + 1;
            jminus = j - 1;
            jplus = j + 1;

            if (iminus >= 0 && jminus >= 0)
            {
                bluavg += image[iminus][jminus].rgbtBlue;
                grnavg += image[iminus][jminus].rgbtGreen;
                redavg += image[iminus][jminus].rgbtRed;
                n++;
            }

            if (iminus >= 0)
            {
                bluavg += image[iminus][j].rgbtBlue;
                grnavg += image[iminus][j].rgbtGreen;
                redavg += image[iminus][j].rgbtRed;
                n++;
            }

            if (iminus >= 0 && jplus < width)
            {
                bluavg += image[iminus][jplus].rgbtBlue;
                grnavg += image[iminus][jplus].rgbtGreen;
                redavg += image[iminus][jplus].rgbtRed;
                n++;
            }

            if (jminus >= 0)
            {
                bluavg += image[i][jminus].rgbtBlue;
                grnavg += image[i][jminus].rgbtGreen;
                redavg += image[i][jminus].rgbtRed;
                n++;
            }

            bluavg += image[i][j].rgbtBlue;
            grnavg += image[i][j].rgbtGreen;
            redavg += image[i][j].rgbtRed;
            n++;

            if (jplus < width)
            {
                bluavg += image[i][jplus].rgbtBlue;
                grnavg += image[i][jplus].rgbtGreen;
                redavg += image[i][jplus].rgbtRed;
                n++;
            }

            if (iplus < height && jminus >= 0)
            {
                bluavg += image[iplus][jminus].rgbtBlue;
                grnavg += image[iplus][jminus].rgbtGreen;
                redavg += image[iplus][jminus].rgbtRed;
                n++;
            }

            if (iplus < height)
            {
                bluavg += image[iplus][j].rgbtBlue;
                grnavg += image[iplus][j].rgbtGreen;
                redavg += image[iplus][j].rgbtRed;
                n++;
            }

            if (iplus < height && jplus < width)
            {
                bluavg += image[iplus][jplus].rgbtBlue;
                grnavg += image[iplus][jplus].rgbtGreen;
                redavg += image[iplus][jplus].rgbtRed;
                n++;
            }

            if (round((float)bluavg / n) > 255)
            {
                tmparr[i][j].rgbtBlue = 255;
            }
            else
            {
                tmparr[i][j].rgbtBlue = round((float)bluavg / n);
            }

            if (round((float)grnavg / n) > 255)
            {
                tmparr[i][j].rgbtGreen = 255;
            }
            else
            {
            tmparr[i][j].rgbtGreen = round((float)grnavg / n);
            }

            if (round((float)redavg / n) > 255)
            {
                tmparr[i][j].rgbtRed = 255;
            }
            else
            {
            tmparr[i][j].rgbtRed = round((float)redavg / n);
            }

            bluavg = 0;
            grnavg = 0;
            redavg = 0;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tmparr[i][j];
        }
    }
    return;
}
