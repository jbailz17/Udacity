from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

category1 = Category(name="Soccer", user_id=1)
session.add(category1)
session.commit()

category2 = Category(name="Basketball",  user_id=1)
session.add(category2)
session.commit()

category3 = Category(name="Baseball",  user_id=1)
session.add(category3)
session.commit()

category4 = Category(name="Frisbee",  user_id=1)
session.add(category4)
session.commit()

category5 = Category(name="Snowboarding", user_id=1)
session.add(category5)
session.commit()

category6 = Category(name="Rock Climbing",user_id=1)
session.add(category6)
session.commit()

category7 = Category(name="Foosball",  user_id=1)
session.add(category7)
session.commit()

category8 = Category(name="Skating", user_id=1)
session.add(category8)
session.commit()

category9 = Category(name="Hockey",  user_id=1)
session.add(category9)
session.commit()

item1 = Item(category_id=5, name="Goggles",
             description="Protective snow goggles.",
             user_id=1)
session.add(item1)
session.commit()

item2 = Item(category_id=5, name="Snowboard",
             description="Sleek, Fast, high end snowboard.",
             user_id=1)
session.add(item2)
session.commit()

print "Filled Database!"
