from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql+psycopg2://postgres:postgres@localhost:5432/automacao_leads"