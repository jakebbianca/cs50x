#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

#define TRUE 1
#define FALSE 0

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
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool cycle_check(int loser, int origin);

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
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (!strcmp(name, candidates[i]))
        {
            continue;
        }
        else
        {
            // Voter's rankth preference is candidate i from candidates[]
            // ranks[] is an array of integers, so it should accept inteegers and not actual strings
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] == preferences[j][i])
            {
                continue;
            }
            else if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (preferences[j][i] > preferences[i][j])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // Copy relevant pairs from pairs array
    pair max;
    int tmpindex;

    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count; j++)
        {
            max.winner = pairs[i].winner;
            max.loser = pairs[i].loser;

            if (preferences[pairs[i].winner][pairs[i].loser] < preferences[pairs[i].winner][pairs[i].loser])
            {
                max.winner = pairs[j].winner;
                max.loser = pairs[j].loser;
                tmpindex = j;
            }

        if (max.winner == pairs[i].winner && max.loser == pairs[i].loser)
        {
            continue;
        }
        else
        {
            pairs[tmpindex].winner = pairs[i].winner;
            pairs[tmpindex].loser = pairs[i].loser;
            pairs[i].winner = max.winner;
            pairs[i].loser = max.loser;
        }
        }
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    locked[pairs[0].winner][pairs[0].loser] = TRUE;

    for (int i = 1; i < pair_count; i++)
    {
        if (cycle_check(pairs[i].loser, pairs[i].winner) == FALSE)
        {
            locked[pairs[i].winner][pairs[i].loser] = TRUE;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        int j = i;

        while (j < candidate_count)
        {
            if (locked[j][i] == FALSE)
            {
                j++;
            }
            else
            {
                break;
            }
        }
        if (j == candidate_count)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
    printf("Failure to print the winner.");
    return;
}

// Check if adding an edge will cause a cycle
bool cycle_check(int loser, int origin)
{

    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i] == TRUE)
        {
            if (i == origin)
            {
                return TRUE;
            }
            else if (cycle_check(i, origin) == TRUE)
            {
                return TRUE;
            }
        }
    }

    return false;
}

