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

The program was created taking under account needs in certain company in certain job, so it may not be suitable for otcher organisations, but still may be helpful in some way, especially after some adapting changes. 



