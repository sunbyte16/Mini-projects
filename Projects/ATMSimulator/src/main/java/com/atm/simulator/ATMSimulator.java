package com.atm.simulator;

import java.util.*;

public class ATMSimulator {
    private static Map<String, Account> accounts = new HashMap<>();
    private static Scanner scanner = new Scanner(System.in);
    private static Account currentAccount = null;

    public static void main(String[] args) {
        initializeAccounts();
        showWelcomeScreen();
        scanner.close();
    }

    private static void initializeAccounts() {
        // Pre-populate with some test accounts
        accounts.put("1234567890", new Account("ACC1001", "1234567890", 1234, 5000.0));
        accounts.put("9876543210", new Account("ACC1002", "9876543210", 4321, 2500.0));
    }

    private static void showWelcomeScreen() {
        while (true) {
            System.out.println("\n=== Welcome to Java ATM ===");
            System.out.print("Enter your card number (or 'exit' to quit): ");
            String cardNumber = scanner.nextLine().trim();
            
            if (cardNumber.equalsIgnoreCase("exit")) {
                System.out.println("Thank you for using Java ATM. Goodbye!");
                return;
            }

            if (authenticateUser(cardNumber)) {
                showMainMenu();
                currentAccount = null; // Logout
            } else {
                System.out.println("Invalid card number or PIN. Please try again.");
            }
        }
    }

    private static boolean authenticateUser(String cardNumber) {
        if (!accounts.containsKey(cardNumber)) {
            return false;
        }

        int attempts = 3;
        while (attempts > 0) {
            System.out.print("Enter your 4-digit PIN (" + attempts + " attempts remaining): ");
            try {
                int pin = Integer.parseInt(scanner.nextLine());
                if (accounts.get(cardNumber).validatePin(pin)) {
                    currentAccount = accounts.get(cardNumber);
                    return true;
                } else {
                    System.out.println("Incorrect PIN. Please try again.");
                    attempts--;
                }
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter numbers only.");
            }
        }
        System.out.println("Too many failed attempts. Card blocked.");
        return false;
    }

    private static void showMainMenu() {
        boolean sessionActive = true;
        while (sessionActive && currentAccount != null) {
            System.out.println("\n=== Main Menu ===");
            System.out.println("Card: " + currentAccount.getMaskedCardNumber());
            System.out.println("1. Check Balance");
            System.out.println("2. Withdraw Cash");
            System.out.println("3. Deposit Money");
            System.out.println("4. View Transaction History");
            System.out.println("5. Change PIN");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");

            try {
                int choice = Integer.parseInt(scanner.nextLine());
                switch (choice) {
                    case 1:
                        checkBalance();
                        break;
                    case 2:
                        withdrawCash();
                        break;
                    case 3:
                        depositMoney();
                        break;
                    case 4:
                        viewTransactionHistory();
                        break;
                    case 5:
                        changePin();
                        break;
                    case 6:
                        System.out.println("Thank you for using Java ATM. Please take your card.");
                        sessionActive = false;
                        break;
                    default:
                        System.out.println("Invalid choice. Please try again.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
            }
        }
    }

    private static void checkBalance() {
        System.out.printf("\nYour current balance is: $%.2f%n", currentAccount.getBalance());
    }

    private static void withdrawCash() {
        System.out.println("\n=== Withdraw Cash ===");
        System.out.println("1. $20\t2. $40\t3. $60");
        System.out.println("4. $100\t5. $200\t6. Other amount");
        System.out.println("7. Cancel");
        System.out.print("Enter your choice: ");

        try {
            int choice = Integer.parseInt(scanner.nextLine());
            double amount = 0;

            switch (choice) {
                case 1: amount = 20; break;
                case 2: amount = 40; break;
                case 3: amount = 60; break;
                case 4: amount = 100; break;
                case 5: amount = 200; break;
                case 6:
                    System.out.print("Enter amount to withdraw: $");
                    amount = Double.parseDouble(scanner.nextLine());
                    break;
                case 7:
                    return;
                default:
                    System.out.println("Invalid choice.");
                    return;
            }

            if (amount > 0) {
                if (currentAccount.withdraw(amount)) {
                    System.out.printf("Please take your $%.2f\n", amount);
                    System.out.printf("New balance: $%.2f\n", currentAccount.getBalance());
                } else {
                    System.out.println("Insufficient funds or invalid amount.");
                }
            } else {
                System.out.println("Invalid amount. Please enter a positive number.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid input. Please enter numbers only.");
        }
    }

    private static void depositMoney() {
        System.out.print("\nEnter amount to deposit: $");
        try {
            double amount = Double.parseDouble(scanner.nextLine());
            if (amount > 0) {
                currentAccount.deposit(amount);
                System.out.printf("$%.2f has been deposited successfully.%n", amount);
                System.out.printf("New balance: $%.2f%n", currentAccount.getBalance());
            } else {
                System.out.println("Invalid amount. Please enter a positive number.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid input. Please enter numbers only.");
        }
    }

    private static void viewTransactionHistory() {
        List<Transaction> transactions = currentAccount.getTransactionHistory();
        System.out.println("\n=== Transaction History ===");
        System.out.println(Transaction.getHeader());
        System.out.println("-".repeat(60));
        
        for (Transaction t : transactions) {
            System.out.println(t);
        }
        
        if (transactions.isEmpty()) {
            System.out.println("No transactions found.");
        }
    }

    private static void changePin() {
        System.out.println("\n=== Change PIN ===");
        try {
            System.out.print("Enter current 4-digit PIN: ");
            int currentPin = Integer.parseInt(scanner.nextLine());
            
            System.out.print("Enter new 4-digit PIN: ");
            int newPin = Integer.parseInt(scanner.nextLine());
            
            System.out.print("Confirm new 4-digit PIN: ");
            int confirmPin = Integer.parseInt(scanner.nextLine());
            
            if (newPin != confirmPin) {
                System.out.println("New PINs do not match.");
                return;
            }
            
            if (String.valueOf(newPin).length() != 4) {
                System.out.println("PIN must be 4 digits.");
                return;
            }
            
            if (currentAccount.changePin(currentPin, newPin)) {
                System.out.println("PIN changed successfully.");
            } else {
                System.out.println("Incorrect current PIN.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid input. Please enter numbers only.");
        }
    }
}
