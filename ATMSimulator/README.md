# ATM Simulator

A Java console-based ATM Simulator that mimics basic banking operations with PIN validation.

## Features

- Account authentication with PIN
- Check account balance
- Deposit money
- Withdraw money
- View transaction history
- Change PIN
- Simple and secure console interface

## Prerequisites

- Java Development Kit (JDK) 8 or higher

## How to Run

1. Navigate to the project directory
2. Compile the Java files:
   ```
   javac src/main/java/com/atm/simulator/*.java -d target/classes
   ```
3. Run the application:
   ```
   java -cp target/classes com.atm.simulator.ATMSimulator
   ```

## Default Accounts

For testing purposes, the following accounts are pre-configured:
- Card Number: 1234567890, PIN: 1234, Balance: 5000.0
- Card Number: 9876543210, PIN: 4321, Balance: 2500.0

## Project Structure

```
src/main/java/com/atm/simulator/
├── Account.java           # Account entity class
├── Transaction.java       # Transaction record class
└── ATMSimulator.java      # Main application class
```

## Usage

1. Enter your card number and PIN
2. Select an operation from the menu
3. Follow the on-screen instructions
4. Logout when done
