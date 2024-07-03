from sqlalchemy import create_engine,MetaData

engine = create_engine("mysql+pymysql://root:sebastian2810@localhost:3306/python")
meta = MetaData()
conn = engine.connect()