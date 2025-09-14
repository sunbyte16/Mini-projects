#!/usr/bin/env python3
"""
Unit Converter - A command-line tool for converting between different units of measurement.

This program allows users to convert between various units of measurement including
length, weight, temperature, time, and optionally currency.
"""

import os
import json
import csv
from datetime import datetime

# Conversion functions for different categories
def convert_length(value, from_unit, to_unit):
    """Convert between length units."""
    # Conversion rates to meters (base unit)
    to_meter = {
        'meters': 1,
        'kilometers': 1000,
        'miles': 1609.34,
        'feet': 0.3048,
        'inches': 0.0254,
        'centimeters': 0.01
    }
    
    # Convert from the original unit to meters, then to the target unit
    meters = value * to_meter[from_unit]
    result = meters / to_meter[to_unit]
    
    return round(result, 2)

def convert_weight(value, from_unit, to_unit):
    """Convert between weight units."""
    # Conversion rates to grams (base unit)
    to_gram = {
        'kilograms': 1000,
        'grams': 1,
        'pounds': 453.592,
        'ounces': 28.3495,
        'tonnes': 1000000
    }
    
    # Convert from the original unit to grams, then to the target unit
    grams = value * to_gram[from_unit]
    result = grams / to_gram[to_unit]
    
    return round(result, 2)

def convert_temperature(value, from_unit, to_unit):
    """Convert between temperature units."""
    # First convert to Celsius as the intermediate unit
    if from_unit == 'celsius':
        celsius = value
    elif from_unit == 'fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'kelvin':
        celsius = value - 273.15
    
    # Then convert from Celsius to the target unit
    if to_unit == 'celsius':
        result = celsius
    elif to_unit == 'fahrenheit':
        result = (celsius * 9/5) + 32
    elif to_unit == 'kelvin':
        result = celsius + 273.15
    
    return round(result, 2)

def convert_time(value, from_unit, to_unit):
    """Convert between time units."""
    # Conversion rates to seconds (base unit)
    to_second = {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'days': 86400
    }
    
    # Convert from the original unit to seconds, then to the target unit
    seconds = value * to_second[from_unit]
    result = seconds / to_second[to_unit]
    
    return round(result, 2)

def convert_currency(value, from_unit, to_unit):
    """Convert between currency units using static rates."""
    # Static conversion rates to USD (base unit)
    # Note: These rates are static and would need to be updated manually
    to_usd = {
        'usd': 1,
        'eur': 1.18,  # 1 EUR = 1.18 USD (example rate)
        'gbp': 1.38,  # 1 GBP = 1.38 USD (example rate)
        'jpy': 0.0091, # 1 JPY = 0.0091 USD (example rate)
        'cad': 0.80   # 1 CAD = 0.80 USD (example rate)
    }
    
    # Convert from the original currency to USD, then to the target currency
    usd = value * to_usd[from_unit]
    result = usd / to_usd[to_unit]
    
    return round(result, 2)

# Available units for each category
AVAILABLE_UNITS = {
    'length': ['meters', 'kilometers', 'miles', 'feet', 'inches', 'centimeters'],
    'weight': ['kilograms', 'grams', 'pounds', 'ounces', 'tonnes'],
    'temperature': ['celsius', 'fahrenheit', 'kelvin'],
    'time': ['seconds', 'minutes', 'hours', 'days'],
    'currency': ['usd', 'eur', 'gbp', 'jpy', 'cad']
}

# Mapping of categories to their conversion functions
CONVERSION_FUNCTIONS = {
    'length': convert_length,
    'weight': convert_weight,
    'temperature': convert_temperature,
    'time': convert_time,
    'currency': convert_currency
}

def save_conversion_to_log(category, value, from_unit, to_unit, result):
    """Save the conversion details to a log file."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        'timestamp': timestamp,
        'category': category,
        'value': value,
        'from_unit': from_unit,
        'to_unit': to_unit,
        'result': result
    }
    
    # Save as JSON
    json_log_path = os.path.join(log_dir, 'conversion_log.json')
    try:
        if os.path.exists(json_log_path):
            with open(json_log_path, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(json_log_path, 'w') as f:
            json.dump(logs, f, indent=4)
    except Exception as e:
        print(f"Error saving to JSON log: {e}")
    
    # Save as CSV
    csv_log_path = os.path.join(log_dir, 'conversion_log.csv')
    try:
        file_exists = os.path.exists(csv_log_path)
        with open(csv_log_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=log_entry.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry)
    except Exception as e:
        print(f"Error saving to CSV log: {e}")

def display_menu():
    """Display the main menu of the unit converter."""
    print("\n===== UNIT CONVERTER =====")
    print("1. Length Conversion")
    print("2. Weight Conversion")
    print("3. Temperature Conversion")
    print("4. Time Conversion")
    print("5. Currency Conversion")
    print("6. Exit")
    return input("Enter your choice (1-6): ")

def get_numeric_input(prompt):
    """Get and validate numeric input from the user."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def get_unit_input(category, prompt):
    """Get and validate unit input from the user."""
    units = AVAILABLE_UNITS[category]
    print(f"Available {category} units: {', '.join(units)}")
    
    while True:
        unit = input(prompt).lower()
        if unit in units:
            return unit
        print(f"Error: Invalid unit. Please choose from: {', '.join(units)}")

def perform_conversion():
    """Main function to handle the conversion process."""
    while True:
        choice = display_menu()
        
        if choice == '6':
            print("Thank you for using the Unit Converter. Goodbye!")
            break
        
        category_map = {
            '1': 'length',
            '2': 'weight',
            '3': 'temperature',
            '4': 'time',
            '5': 'currency'
        }
        
        if choice not in category_map:
            print("Invalid choice. Please enter a number between 1 and 6.")
            continue
        
        category = category_map[choice]
        
        # Get user input for the conversion
        value = get_numeric_input(f"Enter the {category} value to convert: ")
        from_unit = get_unit_input(category, f"Convert from ({', '.join(AVAILABLE_UNITS[category])}): ")
        to_unit = get_unit_input(category, f"Convert to ({', '.join(AVAILABLE_UNITS[category])}): ")
        
        # Perform the conversion
        try:
            convert_func = CONVERSION_FUNCTIONS[category]
            result = convert_func(value, from_unit, to_unit)
            
            # Display the result
            print(f"\nResult: {value} {from_unit} = {result} {to_unit}")
            
            # Ask if user wants to save this conversion to log
            save_log = input("Do you want to save this conversion to log? (y/n): ").lower()
            if save_log == 'y':
                save_conversion_to_log(category, value, from_unit, to_unit, result)
                print("Conversion saved to log.")
        
        except Exception as e:
            print(f"Error during conversion: {e}")
        
        # Ask if user wants to perform another conversion
        another = input("\nDo you want to perform another conversion? (y/n): ").lower()
        if another != 'y':
            print("Thank you for using the Unit Converter. Goodbye!")
            break

if __name__ == "__main__":
    print("Welcome to the Unit Converter!")
    print("This program allows you to convert between different units of measurement.")
    perform_conversion()