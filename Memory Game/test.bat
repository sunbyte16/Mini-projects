@echo off
echo Testing Memory Game compilation and basic functionality...
echo.

REM Test compilation
echo Compiling...
gcc -Wall -Wextra -std=c99 -o memory_game_test main.c
if errorlevel 1 (
    echo Compilation failed!
    exit /b 1
)

echo Compilation successful!
echo.
echo Game executable created: memory_game_test.exe
echo.
echo To play the game, run: memory_game_test.exe
echo.
echo Game features:
echo - 4x4 grid with 16 cards
echo - 8 pairs of numbers (1-8)
echo - Flip 2 cards per turn
echo - Match all pairs to win
echo.
pause