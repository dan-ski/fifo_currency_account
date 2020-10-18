import sqlite3

from fifobasic import FifoBasic


class DbCommunication(object):

    def create_connection(self, db_name):
        """sets connection with given database file"""

        conn = sqlite3.connect(db_name)

        print("Utworzono połączenie z: ", db_name, "\n")

        return conn

    def check_if_table(self, conn, table_name):
        cursor = conn.cursor()
        requested_table = ('{}'.format(table_name),)
        cursor.execute("""SELECT count(name)from sqlite_master WHERE type = 'table' AND
                       name=?""", requested_table)
        if cursor.fetchone()[0] == 1:
            print("Tabela o nazwie ", table_name, " już istnieje")
            return True
        else:
            return False

    def accounts_list(self, conn):
        cursor = conn.cursor()
        sql = "SELECT name from sqlite_master WHERE type = 'table' "
        cursor.execute(sql)
        all_tables = cursor.fetchall()
        if all_tables is None:
            return
        account_list = []
        n = 1
        for table_name in all_tables:
            table_name_str = str(table_name)
            if "history" not in table_name_str:
                table_name_str = table_name_str.replace("(", "")
                table_name_str = table_name_str.replace(")", "")
                table_name_str = table_name_str.replace("'", "")
                table_name_str = table_name_str.replace(",", "")
                account_list.append(table_name_str)
                print(n, ": ", table_name_str)
                n += 1
        return account_list

    def new_tables(self, conn, currency, given_name):
        cursor = conn.cursor()

        title = "Fifo_"+currency+"_"+given_name
        title_tr_history = title+"_tr_history"
        title_set_history = title+"_set_history"

        answer = "t"
        fifo_basic = FifoBasic()

        while self.check_if_table(conn, title):

            answer = fifo_basic.yes_or_no("Czy utworzyć nowy rejestr bankowy? (t/n)", ["t", "n"])

            if answer == "t":
                given_name = input("Proszę podać inną nazwę rejestru: ")
                title = "Fifo_"+currency+"_"+given_name
                # contains history of transactions
                title_tr_history = "Fifo_"+currency+"_"+given_name+"_tr_history"
                # contains hisotry of currency settelment
                title_set_history = "Fifo_"+currency+"_"+given_name+"_set_history"
            else:
                break

        if answer == "t":
            cursor.execute("CREATE TABLE "+title+"(rate smallmoney, value money, operation_date date, rate_date date)")
            cursor.execute("CREATE TABLE "+title_tr_history+"(rate smallmoney, value money, operation_date date, "
                                                            "rate_date date)")
            cursor.execute("CREATE TABLE "+title_set_history+"(rate smallmoney, set_value money, incoming_date date, "
                                                             "rate_date date, outgoing_amount money, "
                                                             "operation_date date)")
            print("Utworzono rejestr: ", title)
            print("Utworzono rejestr: ", title_tr_history)
            print("Utworzono rejestr: ", title_set_history)


class BankAccount(DbCommunication):

    def __init__(self, conn, table_name):
        self.conn = conn
        self.table_name = table_name

    # Adds an incoming transaction to bank statement
    def add_incoming(self, transaction_data):

        fifo_basic = FifoBasic()

        choice = fifo_basic.yes_or_no("Zastosować kurs ostatniego dnia roboczego przed transakcją? [t/n]", ["t", "n"])

        if choice == "n":
            transaction_data[0] = fifo_basic.provide_float("Proszę podaj kurs waluty "
                                                           "(do czterech miejsc po przecinku): ")

        # access to columns through index and names
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        sql = """insert into {}(rate, value, operation_date, rate_date) values
                        (?,?,?,?)""".format(self.table_name)
        cursor.execute(sql, transaction_data)
        self.conn.commit()
        print("Dodano wpis do rejestru: ", self.table_name)
        self.add_history(self.conn, self.table_name, transaction_data)

    # shows current account balance
    def currency_sum(self):

        # access to columns through index and names
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        sql = " select sum(value) from {}".format(self.table_name)
        cursor.execute(sql)
        result = cursor.fetchone()[0]

        if result:
            return result
        else:
            return 0

    def find_min(self):
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        sql_row_id = """ SELECT rowid from {}
                        WHERE rate_date =(SELECT MIN(rate_date) FROM {})
                        AND rate_date > 0""".format(self.table_name, self.table_name)
        cursor.execute(sql_row_id)
        oldest_row_id = cursor.fetchone()[0]

        sql = """ SELECT * from {} WHERE rowid = {} """.format(self.table_name, oldest_row_id)
        cursor.execute(sql)
        oldest_transaction = tuple(cursor.fetchone())

        print("Oldest row id: ", oldest_row_id)
        transaction_data = [oldest_transaction, oldest_row_id]
        return transaction_data

    def update_value(self, new_value, row_id):

        # access to columns through index and names
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        change = (new_value, row_id)

        sql = "UPDATE {} SET value = ? WHERE rowid = ?".format(self.table_name)
        cursor.execute(sql, change)
        self.conn.commit()

    def delete_empty_rows(self):

        # access to columns through index and names
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        sql = "DELETE FROM {} WHERE value = 0".format(self.table_name)
        cursor.execute(sql)
        self.conn.commit()

        print("Usunięto wiersze z wartością zero.")

    def add_outgoing(self, transaction_data):

        # access to columns through index and names
        self.conn.row_factory = sqlite3.Row
        transaction_value = transaction_data[1]
        outgoing_date = transaction_data[2]

        if transaction_value > self.currency_sum():
            print("Ilość waluty na rachunku jest zbyt mała na pokrycie transakcji wychodzącej.")
            return

        amount_to_go = transaction_value

        while amount_to_go > 0:
            oldest_row = self.find_min()[0]
            oldest_row_id = self.find_min()[1]
            oldest_rate = oldest_row[0]
            oldest_value = oldest_row[1]
            oldest_oper_date = oldest_row[2]
            oldest_rate_date = oldest_row[3]
            if oldest_value <= amount_to_go:
                amount_to_go -= oldest_value
                self.update_value(0, oldest_row_id)
                self.delete_empty_rows()
                print("Rozliczono", oldest_value, "po kursie", oldest_rate)
                self.add_set_history(self.conn, self.table_name, oldest_rate, oldest_value, oldest_oper_date,
                                     oldest_rate_date, transaction_value, outgoing_date)
            else:
                oldest_value -= amount_to_go
                self.update_value(oldest_value, oldest_row_id)
                print("Rozliczono", amount_to_go, "po kursie", oldest_rate)
                self.add_set_history(self.conn, self.table_name, oldest_rate, amount_to_go, oldest_oper_date,
                                     oldest_rate_date, transaction_value, outgoing_date)
                amount_to_go = 0
        transaction_data[1] = transaction_data[1]*-1
        self.add_history(self.conn, self.table_name, transaction_data)

    # sprawdzić, czy funkcja działa
    def add_history(self, conn, table_name, transaction_data):

        title_tr_history = table_name+"_tr_history"

        # access to columns through index and names
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        sql = """insert into {}(rate, value, operation_date, rate_date) values
                        (?,?,?,?)""".format(title_tr_history)
        cursor.execute(sql, transaction_data)
        conn.commit()

        print("Dodano wpis do rejestru: ", title_tr_history)

    def show_all(self, conn, table_name):

        # access to columns through index and names
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT * FROM {}".format(table_name)
        cursor.execute(sql)
        row = cursor.fetchone()
        print(row.keys())
        print(tuple(row))

        all_rows = cursor.fetchall()
        for row in all_rows:
            if row:
                print(tuple(row))

    def show_history(self, choice):
        """ wyświetla historię transakcji z określonego zakresu dat"""
        if choice == 3:
            transaction_history_table = self.table_name + "_tr_history"
        if choice == 4:
            transaction_history_table = self.table_name + "_set_history"
        fifo_basic = FifoBasic()

        answer = fifo_basic.yes_or_no("Wyświetlić całą historię? (t/n) ", ["t", "n"])
        if answer == "t":
            self.show_all(self.conn, transaction_history_table)

        else:
            print("Proszę podaj datę początkową.")
            start_date = fifo_basic.provide_date()

            print("Proszę podaj datę koncową.")
            end_date = fifo_basic.provide_date()

            # access to columns through index and names
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            sql = "SELECT * FROM {} WHERE operation_date >= ? AND operation_date <= ?".format(transaction_history_table)
            cursor.execute(sql, (start_date, end_date))

            row = cursor.fetchone()
            print(row.keys())
            print(tuple(row))

            all_rows = cursor.fetchall()
            for row in all_rows:
                if row:
                    print(tuple(row))

    def add_set_history(self, conn, table_name, rate, set_value, incoming_date, rate_date, outgoing_amount,
                        operation_date):

        title_set_history = table_name+"_set_history"

        # access to columns through index and names
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        sql = """insert into {}(rate, set_value, incoming_date, rate_date, outgoing_amount, operation_date) values
                        (?,?,?,?,?,?)""".format(title_set_history)
        cursor.execute(sql, (rate, set_value, incoming_date, rate_date, outgoing_amount, operation_date))
        conn.commit()

        print("Dodano wpis do rejestru: ", title_set_history)
