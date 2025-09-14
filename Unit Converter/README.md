# 🔄 Unit Converter

A command-line tool for converting between different units of measurement including length, weight, temperature, time, and currency.

## ✨ Features

- **Multiple Conversion Categories**:
  - 📏 Length (meters, kilometers, miles, feet, inches, centimeters)
  - ⚖️ Weight (kilograms, grams, pounds, ounces, tonnes)
  - 🌡️ Temperature (Celsius, Fahrenheit, Kelvin)
  - ⏱️ Time (seconds, minutes, hours, days)
  - 💱 Currency (USD, EUR, GBP, JPY, CAD) with static conversion rates

- **User-Friendly Interface**:
  - 📋 Menu-driven CLI
  - 📝 Lists available units for each category
  - 🛡️ Handles invalid inputs gracefully

- **Additional Features**:
  - 🔢 Results rounded to 2 decimal places
  - 💾 Option to save conversion history to log files (JSON and CSV)
  - 🔄 Multiple conversions in one session

## 📋 Requirements

- 🐍 Python 3.6 or higher

## 🔧 Installation

1. Clone this repository or download the source code
2. Navigate to the project directory

## 📖 Usage

Run the program using Python:

```bash
python main.py
```

Follow the on-screen prompts to:
1. Select a conversion category
2. Enter the value to convert
3. Specify the source and target units
4. View the conversion result
5. Optionally save the conversion to a log file

## 🔍 Example

```
Welcome to the Unit Converter!
This program allows you to convert between different units of measurement.

===== UNIT CONVERTER =====
1. Length Conversion
2. Weight Conversion
3. Temperature Conversion
4. Time Conversion
5. Currency Conversion
6. Exit
Enter your choice (1-6): 1

Enter the length value to convert: 10
Available length units: meters, kilometers, miles, feet, inches, centimeters
Convert from (meters, kilometers, miles, feet, inches, centimeters): meters
Convert to (meters, kilometers, miles, feet, inches, centimeters): feet

Result: 10 meters = 32.81 feet

Do you want to save this conversion to log? (y/n): y
Conversion saved to log.

Do you want to perform another conversion? (y/n): n
Thank you for using the Unit Converter. Goodbye!
```

## 📊 Log Files

Conversion logs are stored in the `logs` directory in two formats:
- 📄 `conversion_log.json` - JSON format
- 📄 `conversion_log.csv` - CSV format

Each log entry includes:
- Timestamp
- Conversion category
- Original value and unit
- Target unit
- Conversion result

## 📂 Project Structure

- 📜 `main.py` - Main program file containing all conversion functions and CLI interface
- 📁 `logs/` - Directory for storing conversion logs (created automatically)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Created with ❤️ by Sunil Sharma

[![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-181717?style=for-the-badge&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil_Kumar-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Sunil_Kumar-4285F4?style=for-the-badge&logo=google-chrome)](https://lively-dodol-cc397c.netlify.app)