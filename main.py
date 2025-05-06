import pandas as pd
import numpy as np


class DataImporter:
    @staticmethod
    def load_data(filepath):
        print("Завантаження даних...")
        df = pd.read_csv(filepath)
        print("Дані успішно завантажено.")
        return df


class DataInspector:
    @staticmethod
    def show_head_tail(df):
        print("\n[1.2] Перші 4 записи:")
        print(df.head(4))
        print("\n[1.2] Останні 4 записи:")
        print(df.tail(4))

    @staticmethod
    def shape_info(df):
        rows, cols = df.shape
        print(f"\n[1.3] Розмірність датасету: {rows} рядків, {cols} колонок")

    @staticmethod
    def memory_usage(df):
        memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
        print(f"[1.4] Обсяг оперативної пам'яті: {memory:.2f} МБ")


class DataFilterSorter:
    @staticmethod
    def filter_electronics_men(df):
        print("\n[2.1] Фільтрація: електроніка, куплена чоловіками")
        df["Product line"] = df["Product line"].str.strip().str.lower()
        df["Gender"] = df["Gender"].str.strip().str.lower()
        electronics_male = df[(df["Product line"] == "electronics") & (df["Gender"] == "male")]
        print(electronics_male)
        return electronics_male

    @staticmethod
    def sort_by_unit_price(df):
        print("\n[2.2] Сортування за ціною за одиницю (спадання), топ-5:")
        sorted_df = df.sort_values(by='Unit price', ascending=False)
        print(sorted_df.head(5))

    @staticmethod
    def add_rating_category(df):
        print("\n[2.3] Додавання колонки 'Rating Category'...")

        def categorize(rating):
            if rating > 8:
                return "High"
            elif 6 <= rating <= 8:
                return "Medium"
            else:
                return "Low"

        df["Rating Category"] = df["Rating"].apply(categorize)
        print("Колонка 'Rating Category' додана.")
        return df


class DataGrouper:
    @staticmethod
    def average_total_per_city(df):
        print("\n[3.1] Середня сума покупок по містах:")
        avg = df.groupby("City")["Total"].mean()
        print(avg)
        return avg

    @staticmethod
    def purchase_count_per_city(df):
        print("\n[3.2] Кількість покупок по містах:")
        count = df["City"].value_counts()
        print(count)
        return count


class DataTransformer:
    @staticmethod
    def extract_purchase_hour(df):
        print("\n[4.1] Витяг години з колонки Time у нову колонку 'purchase_hour'")

        df['DateTime'] = df['Date'].astype(str) + ' ' + df['Time'].astype(str)

        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M')

        df['purchase_hour'] = df['DateTime'].dt.hour
        print("Колонка 'purchase_hour' додана.")
        return df

    @staticmethod
    def extract_week_day(df):
        print("\n[4.2] Витяг дня тижня з колонки Date у колонку 'week_day'")

        df['week_day'] = df['DateTime'].dt.day_name()
        print("Колонка 'week_day' додана.")
        return df


class Conclusion:
    @staticmethod
    def make_conclusion():
        print("\n[5] Висновки:")
        print("- Чоловіки активно купують електроніку — доцільно проводити акції саме для цієї категорії.")
        print("- Місто з найбільшою середньою сумою може бути пріоритетним для впровадження нових послуг.")
        print("- Аналіз часу покупки дозволяє розподіляти персонал ефективніше.")
        print("- Категоризація рейтингу дозволяє виявити проблемні точки в асортименті або обслуговуванні.")
        print(
            "- Рекомендації: покращити роботу в пікові години, фокусуватись на товарах з високим попитом, оптимізувати ланцюг поставок.")


def main():
    filepath = "supermarket_sales.csv"

    print("=== Початок обробки даних супермаркету ===")

    df = DataImporter.load_data(filepath)
    DataInspector.show_head_tail(df)
    DataInspector.shape_info(df)
    DataInspector.memory_usage(df)

    electronics_men = DataFilterSorter.filter_electronics_men(df)
    DataFilterSorter.sort_by_unit_price(df)
    df = DataFilterSorter.add_rating_category(df)

    avg_total = DataGrouper.average_total_per_city(df)
    purchase_counts = DataGrouper.purchase_count_per_city(df)

    df = DataTransformer.extract_purchase_hour(df)
    df = DataTransformer.extract_week_day(df)

    Conclusion.make_conclusion()

    print("\n=== ПІДСУМКИ ===")
    print("\nТоп-5 покупок за ціною за одиницю:")
    print(df.sort_values(by='Unit price', ascending=False).head(5)[["Product line", "Gender", "Unit price"]])

    print("\nКількість покупок по містах:")
    print(purchase_counts)

    print("\nСередня сума покупок по містах:")
    print(avg_total)

    print("\nЗавершено. Усі обчислення виконано успішно.")


if __name__ == "__main__":
    main()
