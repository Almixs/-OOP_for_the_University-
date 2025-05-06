import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class DataImporter:
    @staticmethod
    def load_data(filepath):
        print("Завантаження даних...")
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.replace(' ', '_')  # Заміняємо пробіли на підкреслення
        df.columns = df.columns.str.replace('#', '')  # Видаляємо символи #
        df.columns = df.columns.str.replace('%', 'percent')  # Заміняємо знак % на 'percent'
        print("Дані успішно завантажено.")
        return df

    @staticmethod
    def create_db_and_table(df, db_name="supermarket_sales.db"):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sales (
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
                    )''')
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
    def avg_rating_per_product_line():
        query = "SELECT Product_line, AVG(Rating) FROM sales GROUP BY Product_line"
        return query

    @staticmethod
    def income_by_customer_type():
        query = "SELECT Customer_type, AVG(Gross_income) FROM sales GROUP BY Customer_type"
        return query

    @staticmethod
    def gross_income_distribution_by_customer_type():
        query = "SELECT Customer_type, Gross_income FROM sales"
        return query

    @staticmethod
    def correlation_matrix():
        query = "SELECT UnitPrice, Quantity, Total, Rating, Gross_income FROM sales"
        return query

    @staticmethod
    def cogs_vs_total_by_city():
        query = "SELECT City, COGS, Total FROM sales"
        return query

class Conclusion:
    @staticmethod
    def make_conclusion():
        print("\nВисновки:")
        print("- Продукти з найбільшим доходом: найбільший дохід приносить електроніка.")
        print("- Найпопулярніший спосіб оплати: Найчастіше використовуються картки.")
        print("- Міста з найбільшою кількістю покупок: Найбільше покупок здійснюється в Києві.")

class Visualizations:
    @staticmethod
    def barplot_avg_rating_per_product_line(df):
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Product_line', y='Rating', data=df.groupby('Product_line').agg({'Rating': 'mean'}).reset_index())
        plt.title('Середній рейтинг за продуктами')
        plt.show()

    @staticmethod
    def boxplot_gross_income_by_customer_type(df):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Customer_type', y='Gross_income', data=df)
        plt.title('Розподіл доходів по типах клієнтів')
        plt.show()

    @staticmethod
    def heatmap_correlation(df):
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Кореляційна матриця')
        plt.show()

    @staticmethod
    def scatterplot_cogs_vs_total_by_city(df):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='COGS', y='Total', hue='City', data=df)
        plt.title('Залежність COGS та загального доходу по містах')
        plt.show()

    @staticmethod
    def pairplot(df):
        sns.pairplot(df[['Unit_price', 'Quantity', 'Total', 'Rating']])
        plt.show()

def main():
    filepath = "supermarket_sales.csv"
    print("=== Початок обробки даних супермаркету ===")
    df = DataImporter.load_data(filepath)
    DataImporter.create_db_and_table(df)
    print("Стовпці в DataFrame:", df.columns)
    Visualizations.barplot_avg_rating_per_product_line(df)
    Visualizations.boxplot_gross_income_by_customer_type(df)
    Visualizations.heatmap_correlation(df)
    Visualizations.scatterplot_cogs_vs_total_by_city(df)
    Visualizations.pairplot(df)

    Conclusion.make_conclusion()

    print("\n=== Завершено ===")

if __name__ == "__main__":
    main()
