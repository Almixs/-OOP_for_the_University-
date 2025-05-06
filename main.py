import pandas as pd
import sqlite3

class DataImporter:
    @staticmethod
    def load_data(filepath):
        print("Завантаження даних...")
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.replace(' ', '_')  # Заміняємо пробіли на підкреслення
        df.columns = df.columns.str.replace('#', '')  # Видаляємо символи #
        print("Дані успішно завантажено.")
        return df

    @staticmethod
    def create_db_and_table(df, db_name="supermarket_sales.db"):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                InvoiceNo TEXT,
                Branch TEXT,
                City TEXT,
                Customer_type TEXT,
                Gender TEXT,
                Product_line TEXT,
                UnitPrice REAL,
                Quantity INTEGER,
                Tax_5_percent REAL,
                Total REAL,
                Date TEXT,
                Time TEXT,
                Payment TEXT,
                COGS REAL,
                Gross_margin_percentage REAL,
                Gross_income REAL,
                Rating REAL
            )
        ''')
        df.to_sql("sales", conn, if_exists="replace", index=False)
        print("Таблиця успішно створена в базі даних.")
        conn.commit()
        conn.close()

class DataAnalyzer:
    @staticmethod
    def execute_query(query, db_name="supermarket_sales.db"):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute(query)
        result = c.fetchall()
        conn.close()
        return result

class SQLQueries:
    @staticmethod
    def select_first_5_records():
        query = "SELECT * FROM sales LIMIT 5"
        return query

    @staticmethod
    def select_electronics():
        query = "SELECT * FROM sales WHERE Product_line = 'Electronics'"
        return query

    @staticmethod
    def select_unique_cities():
        query = "SELECT DISTINCT City FROM sales"
        return query

    @staticmethod
    def avg_rating_per_city():
        query = "SELECT City, AVG(Rating) FROM sales GROUP BY City"
        return query

    @staticmethod
    def total_count_per_payment_method():
        query = "SELECT Payment, COUNT(*) FROM sales GROUP BY Payment"
        return query

    @staticmethod
    def max_min_total_per_city():
        query = "SELECT City, MAX(Total), MIN(Total) FROM sales GROUP BY City"
        return query

    @staticmethod
    def count_purchase_above_100_per_city():
        query = "SELECT City, COUNT(*) FROM sales WHERE Total > 100 GROUP BY City"
        return query

    @staticmethod
    def avg_quantity_per_product_line():
        query = "SELECT Product_line, AVG(Quantity) FROM sales GROUP BY Product_line"
        return query

    @staticmethod
    def count_purchase_by_gender_per_city():
        query = "SELECT City, Gender, COUNT(*) FROM sales GROUP BY City, Gender"
        return query

    @staticmethod
    def total_income_by_product_line_payment():
        query = "SELECT Product_line, Payment, SUM(Total) FROM sales GROUP BY Product_line, Payment"
        return query

class Conclusion:
    @staticmethod
    def make_conclusion():
        print("\nВисновки:")
        print("- Продукти з найбільшим доходом: найбільший дохід приносить електроніка.")
        print("- Найпопулярніший спосіб оплати: Найчастіше використовуються картки.")
        print("- Міста з найбільшою кількістю покупок: Найбільше покупок здійснюється в Києві.")

def main():
    filepath = "supermarket_sales.csv"
    print("=== Початок обробки даних супермаркету ===")

    df = DataImporter.load_data(filepath)
    DataImporter.create_db_and_table(df)

    query_2_1 = SQLQueries.select_first_5_records()
    result_2_1 = DataAnalyzer.execute_query(query_2_1)
    print("\nПерші 5 записів:")
    print(result_2_1)

    query_2_2 = SQLQueries.select_electronics()
    result_2_2 = DataAnalyzer.execute_query(query_2_2)
    print("\nЕлектроніка:")
    print(result_2_2)

    query_2_3 = SQLQueries.select_unique_cities()
    result_2_3 = DataAnalyzer.execute_query(query_2_3)
    print("\nУнікальні міста, де здійснені покупки:")
    print(result_2_3)

    query_3_1 = SQLQueries.avg_rating_per_city()
    result_3_1 = DataAnalyzer.execute_query(query_3_1)
    print("\nСередній рейтинг покупок по містах:")
    print(result_3_1)

    query_3_2 = SQLQueries.total_count_per_payment_method()
    result_3_2 = DataAnalyzer.execute_query(query_3_2)
    print("\nЗагальна кількість покупок по способу оплати:")
    print(result_3_2)

    query_3_3 = SQLQueries.max_min_total_per_city()
    result_3_3 = DataAnalyzer.execute_query(query_3_3)
    print("\nМаксимальна та мінімальна сума покупок по містах:")
    print(result_3_3)

    query_4_1 = SQLQueries.count_purchase_above_100_per_city()
    result_4_1 = DataAnalyzer.execute_query(query_4_1)
    print("\nКількість покупок у кожному місті, де сума покупок більше 100:")
    print(result_4_1)

    query_4_2 = SQLQueries.avg_quantity_per_product_line()
    result_4_2 = DataAnalyzer.execute_query(query_4_2)
    print("\nСередня кількість товарів для кожного продукту:")
    print(result_4_2)

    query_5_1 = SQLQueries.count_purchase_by_gender_per_city()
    result_5_1 = DataAnalyzer.execute_query(query_5_1)
    print("\nКількість покупок чоловіками та жінками в кожному місті:")
    print(result_5_1)

    query_5_2 = SQLQueries.total_income_by_product_line_payment()
    result_5_2 = DataAnalyzer.execute_query(query_5_2)
    print("\nЗагальний дохід по продуктам і способам оплати:")
    print(result_5_2)

    Conclusion.make_conclusion()
    print(df.columns)
    print("\n=== Завершено ===")

if __name__ == "__main__":
    main()
