# Makefile for Memory Game
CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = memory_game
SOURCE = main.c

# Default target
all: $(TARGET)

# Build the executable
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE)

# Clean up generated files
clean:
	del $(TARGET).exe 2>nul || true

# Run the game
run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run