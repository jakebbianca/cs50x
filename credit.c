#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //Ask for input for credit card number
    long ccnum = get_long("Please enter your credit card number: ");
    //Create a copy of the number variable
    long ccnum1 = ccnum;
    //Create variables to find products to sum for every other digit
    int dig0, digl0, digr0, prod, sum0 = 0;
    do
    {
        //Removes right-most digit from ccnum1, then assigns value of mod10 as dig0
        //This serves to make the first 'other' digit the right-most, then to claim as the remainder in dig0
        dig0 = (ccnum1 / 10) % 10;
        //If the original product has only one digit, make prod that digit
        prod = dig0 * 2;
        //If the product has more than one digit, we must sum all of the digits together
        if (prod >= 10)
        {
            //digl is the left digit, so we must subtract the ones digit from the full product
            digl0 = (prod / 10) % 10;
            //Product should only ever have 2 digits here, so the mod10 gets us the ones/right digit
            digr0 = prod % 10;
            //We use product for this sum so we can use it again after the if condition
            prod = digl0 + digr0;
        }   
        //We sum the totals from the applicable options above, for either 1 or 2 digits
        sum0 = sum0 + prod;
        //We divide the copy number by 100 to remove the two digits handled in the previous loop
        //This also helps to satisfy the upcoming 'while' condition
        ccnum1 = ccnum1 / 100;
    }
    while (ccnum1 > 0);
    //Create int variables for remaining digit sum
    int dig1, sum1 = 0;
    //Create a fresh copy of the input number
    long ccnum2 = ccnum;
    do
    {
        //This time we are starting with the rightmost digit; mod10 gets this digit
        dig1 = ccnum2 % 10;
        sum1 = sum1 + dig1;
        ccnum2 = ccnum2 / 100;
    }
    while (ccnum2 > 0);
    int sum2 = sum0 + sum1;
    //"If the sum from Luhn's FAILS the test, print INVALID"
    if (sum2 % 10 != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        //Calculate the amount of digits in the number
        //Create another copy and a variable for digit count
        int count = 0;
        long ccnum3 = ccnum;
        do
        {
            ccnum3 = ccnum3 / 10;
            count++;
        }
        while (ccnum3 != 0);
        //Find the first two digits of the number given
        long ccnum4 = ccnum;
        do
        {
            ccnum4 = ccnum4 / 10;
        }
        while (ccnum4 >= 100);
        //Create left and right digit variables and separate like before
        int digl1, digr1 = 0;
        digl1 = (ccnum4 / 10) % 10;
        digr1 = ccnum4 % 10;
        if (count == 15 && digl1 == 3 && (digr1 == 4 || digr1 == 7))
        {
            printf("AMEX\n");
        }
        else if (count == 16 && digl1 == 5 && digr1 >= 1 && digr1 <= 5)
        {
            printf("MASTERCARD\n");
        }
        else if ((count == 13 || count == 16) && digl1 == 4)
        {
            printf("VISA\n");
        }
        else printf("INVALID\n");
    }
}   

