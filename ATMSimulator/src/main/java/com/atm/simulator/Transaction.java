package com.atm.simulator;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Transaction {
    private String type;
    private double amount;
    private double balanceAfter;
    private LocalDateTime timestamp;
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public Transaction(String type, double amount, double balanceAfter) {
        this.type = type;
        this.amount = amount;
        this.balanceAfter = balanceAfter;
        this.timestamp = LocalDateTime.now();
    }

    @Override
    public String toString() {
        return String.format("%-20s %12.2f %12.2f %s",
                type,
                amount,
                balanceAfter,
                timestamp.format(formatter));
    }

    public static String getHeader() {
        return String.format("%-20s %12s %12s %s",
                "Type", "Amount", "Balance", "Time");
    }
}
