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


// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmparr[height][width];
    float mirror = ((float)width - 1) / 2;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmparr[i][j] = image[i][width - j - 1];
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

// Convert image to sepia
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmparr[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float gxr = 0;
            float gxg = 0;
            float gxb = 0;
            float gyr = 0;
            float gyg = 0;
            float gyb = 0;
            int im = i - 1;
            int ip = i + 1;
            int jm = j - 1;
            int jp = j + 1;
            float sobred = 0;
            int sobgrn = 0;
            int sobblu = 0;
            //Gx sums
            if (im >= 0 && jm >= 0)
            {
                gxr += ((image[im][jm].rgbtRed) * -1);
                gxg += ((image[im][jm].rgbtGreen) * -1);
                gxb += ((image[im][jm].rgbtBlue) * -1);
            }
            if (jm >= 0)
            {
                gxr += ((image[i][jm].rgbtRed) * -2);
                gxg += ((image[i][jm].rgbtGreen) * -2);
                gxb += ((image[i][jm].rgbtBlue) * -2);
            }
            if (ip < height && jm >= 0)
            {
                gxr += ((image[ip][jm].rgbtRed) * -1);
                gxg += ((image[ip][jm].rgbtGreen) * -1);
                gxb += ((image[ip][jm].rgbtBlue) * -1);
            }
            if (im >= 0 && jp < width)
            {
                gxr += (image[im][jp].rgbtRed);
                gxg += (image[im][jp].rgbtGreen);
                gxb += (image[im][jp].rgbtBlue);
            }
            if (jp < width)
            {
                gxr += ((image[i][jp].rgbtRed) * 2);
                gxg += ((image[i][jp].rgbtGreen) * 2);
                gxb += ((image[i][jp].rgbtBlue) * 2);
            }
            if (ip < height && jp < width)
            {
                gxr += (image[ip][jp].rgbtRed);
                gxg += (image[ip][jp].rgbtGreen);
                gxb += (image[ip][jp].rgbtBlue);
            }
            //Gy sums
            if (im >= 0 && jm >= 0)
            {
                gyr += ((image[im][jm].rgbtRed) * -1);
                gyg += ((image[im][jm].rgbtGreen) * -1);
                gyb += ((image[im][jm].rgbtBlue) * -1);
            }
            if (im >= 0)
            {
                gyr += ((image[im][j].rgbtRed) * -2);
                gyg += ((image[im][j].rgbtGreen) * -2);
                gyb += ((image[im][j].rgbtBlue) * -2);
            }
            if (im >= 0 && jp < width)
            {
                gyr += ((image[im][jp].rgbtRed) * -1);
                gyg += ((image[im][jp].rgbtGreen) * -1);
                gyb += ((image[im][jp].rgbtBlue) * -1);
            }
            if (ip < height && jm >= 0)
            {
                gyr += (image[ip][jm].rgbtRed);
                gyg += (image[ip][jm].rgbtGreen);
                gyb += (image[ip][jm].rgbtBlue);
            }
            if (ip < height)
            {
                gyr += ((image[ip][j].rgbtRed) * 2);
                gyg += ((image[ip][j].rgbtGreen) * 2);
                gyb += ((image[ip][j].rgbtBlue) * 2);
            }
            if (ip < height && jp < width)
            {
                gyr += (image[ip][jp].rgbtRed);
                gyg += (image[ip][jp].rgbtGreen);
                gyb += (image[ip][jp].rgbtBlue);
            }
            //If > 255, = 255, else = Sobel

            if (sqrt((gxr * gxr) + (gyr * gyr)) > 255)
            {
                sobred = 255;
            }
            else
            {
                sobred = sqrt((gxr * gxr) + (gyr * gyr));
            }
            if (sqrt((gxg * gxg) + (gyg * gyg)) > 255)
            {
                sobgrn = 255;
            }
            else
            {
                sobgrn = sqrt((gxg * gxg) + (gyg * gyg));
            }
            if (sqrt((gxb * gxb) + (gyb * gyb)) > 255)
            {
                sobblu = 255;
            }
            else
            {
                sobblu = sqrt((gxb * gxb) + (gyb * gyb));
            }

            tmparr[i][j].rgbtRed = sobred;
            tmparr[i][j].rgbtGreen = sobgrn;
            tmparr[i][j].rgbtBlue = sobblu;

            gxr = 0;
            gxg = 0;
            gxb = 0;
            gyr = 0;
            gyg = 0;
            gyb = 0;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = tmparr[i][j].rgbtRed;
            image[i][j].rgbtGreen = tmparr[i][j].rgbtGreen;
            image[i][j].rgbtBlue = tmparr[i][j].rgbtBlue;
        }
    }
}