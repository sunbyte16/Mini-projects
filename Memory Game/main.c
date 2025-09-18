#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

#define ROWS 4
#define COLS 4
#define TOTAL_CARDS (ROWS * COLS)
#define PAIRS (TOTAL_CARDS / 2)

// Structure to represent a card
typedef struct {
    int value;       // The number/letter on the card
    bool is_flipped; // Whether the card is currently showing
    bool is_matched; // Whether the card has been permanently matched
} Card;

// Global game state
Card board[ROWS][COLS];
int flipped_cards[2][2]; // Store positions of currently flipped cards
int flipped_count = 0;   // Number of cards currently flipped (0, 1, or 2)
int matched_pairs = 0;   // Number of pairs successfully matched

// Function prototypes
void initialize_board();
void shuffle_cards();
void display_board();
void display_instructions();
bool get_player_input(int *row, int *col);
bool flip_card(int row, int col);
bool check_match();
void hide_unmatched_cards();
bool is_game_won();
void clear_screen();
void play_game();

int main() {
    printf("=== MEMORY GAME (Card Flip) ===\n");
    printf("Welcome %s! Let's test your memory!\n\n", "Sunil");
    
    display_instructions();
    
    // Initialize random seed
    srand(time(NULL));
    
    // Start the game
    play_game();
    
    return 0;
}

void initialize_board() {
    // Reset game state
    matched_pairs = 0;
    flipped_count = 0;
    
    // Create pairs of numbers (1-8, each appears twice)
    int values[TOTAL_CARDS];
    for (int i = 0; i < PAIRS; i++) {
        values[i * 2] = i + 1;
        values[i * 2 + 1] = i + 1;
    }
    
    // Shuffle the values
    for (int i = TOTAL_CARDS - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = values[i];
        values[i] = values[j];
        values[j] = temp;
    }
    
    // Assign values to board and initialize card states
    int index = 0;
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            board[i][j].value = values[index++];
            board[i][j].is_flipped = false;
            board[i][j].is_matched = false;
        }
    }
}

void display_board() {
    printf("\n    ");
    for (int j = 0; j < COLS; j++) {
        printf("  %d ", j + 1);
    }
    printf("\n");
    
    for (int i = 0; i < ROWS; i++) {
        printf(" %d  ", i + 1);
        for (int j = 0; j < COLS; j++) {
            if (board[i][j].is_matched || board[i][j].is_flipped) {
                printf(" %2d ", board[i][j].value);
            } else {
                printf(" ## ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

void display_instructions() {
    printf("HOW TO PLAY:\n");
    printf("1. You'll see a 4x4 grid of hidden cards (##)\n");
    printf("2. Each card has a number from 1-8 (each number appears twice)\n");
    printf("3. Flip 2 cards at a time by entering their row and column\n");
    printf("4. If the cards match, they stay revealed\n");
    printf("5. If they don't match, they get hidden again\n");
    printf("6. Match all 8 pairs to win!\n");
    printf("7. Enter row and column numbers (1-4)\n\n");
    printf("Press Enter to start...");
    getchar();
    clear_screen();
}

bool get_player_input(int *row, int *col) {
    printf("Enter row (1-4): ");
    if (scanf("%d", row) != 1) {
        while (getchar() != '\n'); // Clear input buffer
        return false;
    }
    
    printf("Enter column (1-4): ");
    if (scanf("%d", col) != 1) {
        while (getchar() != '\n'); // Clear input buffer
        return false;
    }
    
    // Convert to 0-based indexing
    (*row)--;
    (*col)--;
    
    // Validate input
    if (*row < 0 || *row >= ROWS || *col < 0 || *col >= COLS) {
        printf("Invalid input! Please enter numbers between 1 and 4.\n");
        return false;
    }
    
    // Check if card is already matched or flipped
    if (board[*row][*col].is_matched) {
        printf("This card is already matched! Choose another card.\n");
        return false;
    }
    
    if (board[*row][*col].is_flipped) {
        printf("This card is already flipped! Choose another card.\n");
        return false;
    }
    
    return true;
}

bool flip_card(int row, int col) {
    board[row][col].is_flipped = true;
    flipped_cards[flipped_count][0] = row;
    flipped_cards[flipped_count][1] = col;
    flipped_count++;
    
    printf("You flipped: %d\n", board[row][col].value);
    return true;
}

bool check_match() {
    int row1 = flipped_cards[0][0], col1 = flipped_cards[0][1];
    int row2 = flipped_cards[1][0], col2 = flipped_cards[1][1];
    
    if (board[row1][col1].value == board[row2][col2].value) {
        // Match found!
        board[row1][col1].is_matched = true;
        board[row2][col2].is_matched = true;
        matched_pairs++;
        printf("🎉 MATCH! You found a pair of %d's!\n", board[row1][col1].value);
        return true;
    } else {
        printf("No match. Cards will be hidden again.\n");
        return false;
    }
}

void hide_unmatched_cards() {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            if (!board[i][j].is_matched) {
                board[i][j].is_flipped = false;
            }
        }
    }
}

bool is_game_won() {
    return matched_pairs == PAIRS;
}

void clear_screen() {
    // For Windows
    system("cls");
    // For Unix/Linux (comment out the line above and uncomment below)
    // system("clear");
}

void play_game() {
    initialize_board();
    
    printf("Game started! Find all %d pairs.\n", PAIRS);
    
    while (!is_game_won()) {
        display_board();
        printf("Matched pairs: %d/%d\n", matched_pairs, PAIRS);
        
        // Get first card
        int row1, col1;
        printf("\nFirst card:\n");
        while (!get_player_input(&row1, &col1)) {
            // Keep asking until valid input
        }
        flip_card(row1, col1);
        
        display_board();
        
        // Get second card
        int row2, col2;
        printf("Second card:\n");
        while (!get_player_input(&row2, &col2)) {
            // Keep asking until valid input
        }
        flip_card(row2, col2);
        
        display_board();
        
        // Check for match
        bool is_match = check_match();
        
        if (!is_match) {
            printf("Press Enter to continue...");
            while (getchar() != '\n'); // Clear any remaining input
            getchar(); // Wait for Enter
            hide_unmatched_cards();
        }
        
        // Reset flipped count for next turn
        flipped_count = 0;
        
        printf("\n");
    }
    
    // Game won!
    clear_screen();
    display_board();
    printf("🎊 CONGRATULATIONS! 🎊\n");
    printf("You've matched all %d pairs and won the game!\n", PAIRS);
    printf("Thanks for playing, %s!\n", "Sunil");
}