import asyncio
import random
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import SQLAlchemyError

# ---------- 1. База даних та модель вузлів ----------

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    status = Column(String, nullable=False)

DATABASE_URL = "sqlite+aiosqlite:///nodes.db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# ---------- 2. Отримання списку вузлів ----------

async def get_nodes():
    print("[INFO] Отримання вузлів з бази даних...")
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Node))
            return result.scalars().all()
    except SQLAlchemyError as e:
        print(f"[ERROR] Не вдалося отримати вузли: {e}")
        return []

# ---------- 3. Імітація отримання статусу вузла ----------

async def fetch_status(ip):
    print(f"[INFO] Отримання статусу для IP {ip}...")
    await asyncio.sleep(random.uniform(0.1, 0.5))
    status = random.choice(["online", "offline", "unknown"])
    print(f"[DEBUG] Статус для {ip}: {status}")
    return status

# ---------- 4. Додавання вузлів до бази ----------

async def save_nodes_to_db():
    print("[INFO] Додавання нових вузлів у базу...")
    nodes_data = [
        {"ip_address": "192.168.0.1"},
        {"ip_address": "192.168.0.2"},
        {"ip_address": "10.0.0.1"}
    ]

    try:
        async with AsyncSessionLocal() as session:
            for data in nodes_data:
                status = await fetch_status(data["ip_address"])
                node = Node(ip_address=data["ip_address"], status=status)
                session.add(node)
                print(f"[SUCCESS] Вузол {data['ip_address']} додано зі статусом {status}")
            await session.commit()
            print("[INFO] Всі вузли успішно збережені.")
    except SQLAlchemyError as e:
        print(f"[ERROR] Помилка при збереженні вузлів: {e}")

# ---------- 5. Виведення вузлів з бази ----------

async def show_nodes():
    print("\n[INFO] Список вузлів у базі:")
    nodes = await get_nodes()
    if not nodes:
        print("[WARN] Вузлів не знайдено.")
    for node in nodes:
        print(f"ID: {node.id}, IP: {node.ip_address}, Статус: {node.status}")

# ---------- Головна функція ----------

async def main():
    print("[START] Запуск головної програми...")

    try:
        async with engine.begin() as conn:
            print("[INIT] Створення таблиці nodes...")
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print("[INIT] Таблицю успішно створено.")
    except SQLAlchemyError as e:
        print(f"[ERROR] Помилка ініціалізації таблиці: {e}")
        return

    await save_nodes_to_db()
    await show_nodes()

    print("[END] Завершення програми.")

if __name__ == "__main__":
    asyncio.run(main())
