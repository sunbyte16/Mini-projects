package com.atm.simulator;

import java.util.ArrayList;
import java.util.List;

public class Account {
    private String accountNumber;
    private String cardNumber;
    private int pin;
    private double balance;
    private List<Transaction> transactionHistory;

    public Account(String accountNumber, String cardNumber, int pin, double initialBalance) {
        this.accountNumber = accountNumber;
        this.cardNumber = cardNumber;
        this.pin = pin;
        this.balance = initialBalance;
        this.transactionHistory = new ArrayList<>();
        // Add initial balance transaction
        this.transactionHistory.add(new Transaction("Account Opened", initialBalance, initialBalance));
    }

    public boolean validatePin(int enteredPin) {
        return this.pin == enteredPin;
    }

    public boolean changePin(int oldPin, int newPin) {
        if (validatePin(oldPin)) {
            this.pin = newPin;
            return true;
        }
        return false;
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            transactionHistory.add(new Transaction("Withdrawal", -amount, balance));
            return true;
        }
        return false;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            transactionHistory.add(new Transaction("Deposit", amount, balance));
        }
    }

    public double getBalance() {
        return balance;
    }

    public List<Transaction> getTransactionHistory() {
        return new ArrayList<>(transactionHistory);
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public String getCardNumber() {
        return cardNumber;
    }

    public String getMaskedCardNumber() {
        if (cardNumber.length() <= 4) return "****";
        return "****-****-****-" + cardNumber.substring(cardNumber.length() - 4);
    }
}
