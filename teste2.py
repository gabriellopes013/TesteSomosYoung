from sqlalchemy import create_engine

DATABASE_URI = 'postgresql+psycopg2://username:password@hostname/database'
engine = create_engine(DATABASE_URI)
