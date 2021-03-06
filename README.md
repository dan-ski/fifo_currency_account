# fifo_currency_account
Helps to keep record of bank account transactions in foreign currency. 

## Introduction
The program solves a problem I've come across working as an accoutant. In the bank account data we onlny get information about amout of money in foreign currency, while in Polish accounting we also have to keep track of exchange rate of Polish Zloty (PLN) for every transaction. 

Incoming transaction from certain day gets an exchange rate published by National Bank of Poland (NBP) on last working day before transaction. For example we can have 500 euro on our account, but in detail we can have, for example:
- 100 euro with exchange rate from 2020-09-15: 4,4492
- 200 euro with exchange rate from 2020-09-16: 4,4528
- 200 euro with exchange rate from 2020-09-17: 4,4514
When we have to record an outoing transaction we "take" the amount which came first, using FIFO (First in First Out) rule. So, for example, when we have to pay 150 euro, we "take" 100 euro with exchange rate from 2020-09-15: 4,4492, and 50 euro with exchange rate from 2020-09-16: 4,4528. 

To keep track of the exchange rates we were using Excel spreadsheets inputing data manually. The program helps to automate some proceses, so the task becomes less time consuming and hepls to avoid typical mistakes when inserting data manually. 

The program was created taking under account needs in certain company in certain job, so it may not be suitable for otcher organisations, but still may be helpful in some way, especially after adapting changes.

## Technlologies

The program is created with:
- Python version 3.8.5
- SQLITE version 3.31.1

## Setup

To run this project download file fifo.exe from "dist" folder, and open it. 

## Features

List of current features: 

- enables to register multiple bank accounts
- saves history of transactions
- saves history of transaction settlement
- establishes last workday (taking under account weekends and polish holidays)
- downloads exchange rate of account's currency form National Bank of Poland (Narodowy Bank Polski)
- shows current amout of money on chosen account

To-do list:

- error corrections
- export to Excel spreadsheets
- graphical user interface

## Status

Project in progress. 

## License

This project is licensed under the terms of the MIT license.  

## Contact

Feel free to contact me: szt.danski@gmail.com


