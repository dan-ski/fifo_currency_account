"""Program do ewidencjonowania posiadanej waluty,
 zgodnie z odpowiednimi kursami z dnia wpływu.
 Rozchód waluty zgodnie z metodą FIFO (Pierwsze Przyszło Pierwsze Wyszło).
 Kursy walut- kursy średnie NBP z ostatniego dnia roboczego poprzedzającego wpływ.
 Bilans otwarcia wprowadzamy jako wpływy transakcji z odpowiednimi datami.”"""

from fifobasic import FifoBasic

from datetime import date

from data_base_communication import DbCommunication, BankAccount

print("Program Maciek 1.0\n")


def account_operations(account, rate, operation_date, rate_date):

    choice = 0
    while choice != 5:
        print("""
        1- dodaj transakcję na rachunku
        2- bieżący stan rachunku
        3- historia transakcji
        4- historia rozliczeń
        5- zakończ pracę""")

        fifo_basic = FifoBasic()
        choice = fifo_basic.choose_int("\nProszę wpisz numer odpowiadający danej opcji: ", 5)

        if choice == 1:
            print("Wypływy z konta proszę wprowadzać jako liczby ujemne.")
            amount = 0
            while amount == 0:
                amount = fifo_basic.provide_float("Proszę podać kwotę transakcji: ")
            transaction_data = [rate, amount, operation_date, rate_date]
            if amount > 0:
                account.add_incoming(transaction_data)
            if amount < 0:
                amount *= -1
                transaction_data[1] = amount
                print(amount)
                account.add_outgoing(transaction_data)

        elif choice == 2:
            print("Bieżący stan rachunku to: ", account.currency_sum())

        elif choice == 3:
            print("Historia transakcji:\n")
            account.show_history(choice)

        elif choice == 4:
            print("Historia rozliczeń:\n")
            account.show_history(choice)


def main():

    db_com = DbCommunication()
    conn = db_com.create_connection("currency_data.db")

# funkcja zwraca listę nazw tabel z bazy sql zawierających listę rachunków (pomija tabele z historiami)
# napisać wybór rachunku przez użytkownika lub stworzenie nowego

    all_accounts = db_com.accounts_list(conn)
    accounts_number = len(all_accounts)
    print("0 : nowy rachunek")

    fifo_basic = FifoBasic()

    chosen_account = fifo_basic.choose_int("\nProszę wybierz konto (numer mu odpowiadający):", accounts_number)

    while chosen_account == 0:
        currency = fifo_basic.choose_currency_tab_A()
        name = input("Proszę podaj nazwę rachunku (np. nazwa banku prowadzącego rachunek): ")
        db_com.new_tables(conn, currency, name)
        print("0 : nowy rachunek")
        all_accounts = db_com.accounts_list(conn)
        accounts_number = len(all_accounts)
        chosen_account = fifo_basic.choose_int("Proszę wybierz konto (numer mu odpowiadający):", accounts_number)

    chosen_account_name = all_accounts[chosen_account-1]
    print("\nWybrałeś(aś)", chosen_account_name)

    # getting currency name from table name
    split_name = chosen_account_name.split("_")
    currency = split_name[1]

    account = BankAccount(conn, chosen_account_name)

    today = date.today()
    statement_date = fifo_basic.last_weekday(today)
    question = "\nWprowadzasz wyciąg bankowy z {} ? [t/n]".format(str(statement_date))
    answer = fifo_basic.yes_or_no(question, ["t", "n"])
    if answer == "n":
        statement_date = fifo_basic.provide_date()
        print("Wprowadzasz wyciąg z dnia: ", statement_date)

    last_weekday = fifo_basic.last_weekday(statement_date)
    bank_statement_rate = fifo_basic.nbp_exchange_rate(currency, last_weekday)

    print("\nBieżące saldo rachunku", chosen_account_name, " to: ", account.currency_sum())

    account_operations(account, bank_statement_rate, statement_date, last_weekday)


main()
input("\nAby zakończyć, proszę naciśnij enter")
