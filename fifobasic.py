import datetime
import holidays
import requests
import json


class FifoBasic(object):

    def yes_or_no(self, question, options):
        response = None
        while response not in options:
            response = input(question)
            response.lower()
        return response

    def choose_int(self, question, input_range):
        """Asks user to type a positive integer from specified range"""
        user_input = 0.5
        given_range = list(range(input_range+1))
        while not isinstance(user_input, int) or user_input not in given_range:
            try:
                user_input = int(input(question))
                if user_input not in given_range:
                    print("Proszę podaj liczbę od zera do", input_range)
                    continue
            except ValueError:
                print("Proszę podaj liczbę całkowitą.")
                continue

        #optional: print("Wybrałeś(aś): ", user_input)
        return user_input

    def provide_float(self, question):

        user_input = input(question)
        if "," in user_input:
            user_input= user_input.replace(",", ".")

        user_input = float(user_input)

        while not isinstance(user_input, float):
            user_input = float(input(question))

        return user_input

    def choose_currency_tab_A(self):

        curriencies_tab_A = ["THB", "USD", "AUD", "HKD", "CAD", "NZD", "SGD", "EUR", "HUF", "CHF", "GBP",
                             "UAH", "JPY", "CZK", "DKK", "ISK", "NOK", "SEK", "HRK", "RON", "BGN", "TRY",
                             "ILS", "CLP", "PHP", "MXN", "ZAR", "BRL", "MYR", "RUB", "IDR", "INR", "KRW",
                             "CNY", "SDR(MFW) XDR"]

        print("""
        1- bat(Tajlandia)- THB
        2- dolar amerykański- USD
        3- dolar australijski- AUD
        4- dolar Hongkongu- HKD
        5- dolarkanadyjski- CAD
        6- dolar nowozelandzki NZD
        7- dolar singapurski SGD
        8- euro EUR
        9- forint(Węgry) HUF
        10- frank szwajcarski CHF
        11- funt szterling GBP
        12- hrywna(Ukraina) UAH
        13- jen(Japonia) JPY
        14- korona czeska CZK
        15- korona duńska DKK
        16- korona islandzka ISK
        17- korona norweska NOK
        18- korona szwedzka SEK
        20- kuna(Chorwacja) HRK
        21- lej rumuński RON
        22- lew(Bułgaria) BGN
        23- lira turecka TRY
        24- nowy izraelski szekel ILS
        25- peso chilijskie CLP
        26- peso filipińskie PHP
        27- peso meksykańskie MXN
        28- rand(Republika PołudniowejAfryki) ZAR
        29- real(Brazylia) BRL
        30- ringgit(Malezja) MYR
        31- rubel rosyjski RUB
        32- rupia indonezyjska IDR
        33- rupia indyjska INR
        34- won południowokoreański KRW
        35- yuan renminbi(Chiny) CNY
        36- SDR(MFW) XDR
        """)

        choice = self.choose_int("Proszę podaj liczbę odpowiadają walucie, którą wybierasz: ", 36)
        currency = curriencies_tab_A[choice-1]
        print("Wybrałeś:", currency)
        return currency

    def last_weekday(self, today):

        current_year = datetime.datetime.today().year
        polish_holidays = holidays.Poland(years=current_year).items()

        last_weekday = today - datetime.timedelta(1)

        while last_weekday.weekday() in [5, 6] or last_weekday in polish_holidays:
            last_weekday = last_weekday - datetime.timedelta(1)
        return last_weekday

    def nbp_exchange_rate(self, currency, date):

        url_base = "http://api.nbp.pl/api/exchangerates/rates/a/"
        currency = currency.lower()
        date_str = str(date)
        url = url_base + currency + "/" + date_str + "/"

        r = requests.get(url)
        json_rate = json.loads(r.text)
        rate_data = json_rate["rates"]
        rate_data_0 = rate_data[0]
        table_no = rate_data_0["no"]
        table_date = rate_data_0["effectiveDate"]
        exchange_rate = rate_data_0["mid"]

        print("\nTabela nr: ", table_no)
        print("Z dnia: ", table_date)
        print("1", currency, "= ", exchange_rate)

        return exchange_rate

    def provide_date(self):

        year = self.choose_int("Proszę podaj rok (jako liczbę): ", 2100)
        month = self.choose_int("Proszę podaj miesiąc (jako liczbę): ", 12)
        day = self.choose_int("Proszę podaj dzień miesiąca (jako liczbę): ", 31)
        date = datetime.date(year, month, day)
        return date
