import os

from databases import Database
import sqlalchemy as sql

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = sql.create_engine(DATABASE_URL)
metadata = sql.MetaData()

todos = sql.Table('t_todos', metadata,
                  sql.Column('id', sql.Integer, primary_key=True),
                  sql.Column('title', sql.String(60)),
                  sql.Column('description', sql.String(140)),
                  sql.Column('created_date', sql.DateTime,
                             default=sql.sql.func.now(), nullable=False)

                  )

# databases query builder
database = Database(DATABASE_URL)
