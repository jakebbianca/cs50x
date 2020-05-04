#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void swap(int x, int y);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool cycle_check(int winner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    printf("%d", locked[0][0]);
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int k = 0; k < candidate_count; k++)
    {
        // find candidate to match with name given; if not valid, return false
        if (strcmp(name, candidates[k]) == 0)
        {
            //Read: ranks[rank] is effectively ranks[j] given the context we are using it here; j is being used to get ranked votes
            ranks[rank] = k;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
//Start with candidate ranked 1 (aka ranks[0]) and record preference over worse-ranked candidates, then repeat starting at candidate ranked 2...
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            //e.g. if ranks[] == {3, 0, 2, 4, 1}, this will first update preferences[3][0], preferences [3][2], etc.
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            if (preferences[i][j] < preferences [j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    int const_pair_count = pair_count;
    return;
}

void swap(int x, int y)
{
    int temp = x;
    x = y;
    y = temp;
}

// Sort pairs in decreasing order by strength of victory
//Program starts to fail HERE
void sort_pairs(void)
{
    int strength[pair_count];
    for (int i = 0; i < pair_count; i++)
    {
        strength[i] = preferences[pairs[i].winner][pairs[i].winner] - preferences[pairs[i].loser][pairs[i].winner];
    }
    for (int i = 0; i < pair_count - 1; i++)
    {
       for (int j = i + 1; j < pair_count; j++)
       {
           if (strength[j] > strength[i])
           {
           swap(pairs[i].winner, pairs[j].winner);
           swap(pairs[i].loser, pairs[j].loser);
           swap(strength[i], strength[j]);
           }
       }
    }
}
// Lock pairs into the candidate graph in order, without creating cycles
//Need to recursively check for cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count - 1; i++)
    {
        int pairwinner = sortedpairs[i].winner;
        int pairloser = sortedpairs[i].loser;
        if (cycle_check(pairwinner, pairloser) == false)
        {
            locked[pairwinner][pairwinner] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    int loss_edges[MAX];
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j] == 0)
            {
                loss_edges[j]++;
            }
        }
    }
    for (int k = 0; k < candidate_count; k++)
    {
        if (loss_edges[k] == 0)
        {
            printf("%s", candidates[k]);
        }
    }
    return;
}

bool cycle_check(int winner, int loser)
{
    int origin = winner;
    if (origin == loser)
    {
        return true;
    }
    for (int j = 0; j < candidate_count; j++)
    {
        if (locked[loser][j] == true)
        {
            (cycle_check(origin, j));
        }
    }
    return false;
}