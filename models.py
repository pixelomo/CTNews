from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    content = Column(String)
    published_date = Column(DateTime)
    scraped_date = Column(DateTime)

    def __repr__(self):
        return f"<Article(id={self.id}, title={self.title}, url={self.url}, published_date={self.published_date}, scraped_date={self.scraped_date})>"

engine = create_engine('sqlite:///articles.db')
Base.metadata.create_all(engine)

db_session = scoped_session(sessionmaker(bind=engine))
db = db_session()
