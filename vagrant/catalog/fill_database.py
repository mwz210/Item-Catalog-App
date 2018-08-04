from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User
from passlib.apps import custom_app_context as pwd_context

engine = create_engine('postgresql+psycopg2:///catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Michael Zhang", email="mikezhang118@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
             username='bigfoot118', password_hash=pwd_context.hash('Darkkill12@')
             )
session.add(User1)
session.commit()

# Category Push
category1 = Category(user_id=1, name="Arrays and Lists",
                       description=
                        """Arrays and lists are a type of data structure that
                        stores information linearly. There are two types of arrays:
                        Dynamic Array and Static Array. Static Array has a fixed size,
                        meaning it cannot hold more elements than it was originally
                        made to hold. Dynamic Array is an advanced version of
                        the static array, taking away the restriction of having
                        a fixed size in exchange a bit of performance.
                        """
                      )

session.add(category1)
session.commit()


menuItem1 = Item(user_id=1, category=category1, name="Problem 1",
                 description="Another issue"
                )

session.add(menuItem1)
session.commit()


menuItem2 = Item(user_id=1, category=category1, name="Problem 2",
                 description="Another issue"
                )

session.add(menuItem2)
session.commit()


menuItem3 = Item(user_id=1, category=category1, name="Problem 3",
                 description="Another issue"
                )

session.add(menuItem3)
session.commit()

category2 = Category(user_id=1, name="Linked List",
                       description=
                        """A linked list is a linear data structure where each
                        element is a separate object. Each element (we will call
                        it a node) of a list is comprising of two items - the
                        data and a reference to the next node.
                        """
                      )

session.add(category2)
session.commit()

menuItem1 = Item(user_id=1, category=category2, name="Problem 1",
                 description="Another issue"
                )

session.add(menuItem1)
session.commit()


menuItem2 = Item(user_id=1, category=category2, name="Problem 2",
                 description="Another issue"
                )

session.add(menuItem2)
session.commit()


menuItem3 = Item(user_id=1, category=category2, name="Problem 3",
                 description="Another issue"
                )

session.add(menuItem3)
session.commit()

category3 = Category(user_id=1, name="Stack and Queues",
                       description=
                        """A linked list is a linear data structure where each
                        element is a separate object. Each element (we will call
                        it a node) of a list is comprising of two items - the
                        data and a reference to the next node.
                        """
                      )

session.add(category3)
session.commit()

menuItem1 = Item(user_id=1, category=category3, name="Problem 1",
                 description="Another issue"
                )

session.add(menuItem1)
session.commit()


menuItem2 = Item(user_id=1, category=category3, name="Problem 2",
                 description="Another issue"
                )

session.add(menuItem2)
session.commit()


menuItem3 = Item(user_id=1, category=category3, name="Problem 3",
                 description="Another issue"
                )

session.add(menuItem3)
session.commit()



category4 = Category(user_id=1, name="Bit Manipulation",
                       description=
                        """Bit manipulation is the act of algorithmically
                        manipulating bits or other pieces of data shorter than a
                        word. Computer programming tasks that require bit
                        manipulation include low-level device control, error
                        detection and correction algorithms, data compression,
                        encryption algorithms, and optimization.
                        """
                      )

session.add(category4)
session.commit()

menuItem1 = Item(user_id=1, category=category4, name="Problem 1",
                 description="Another issue"
                )

session.add(menuItem1)
session.commit()


menuItem2 = Item(user_id=1, category=category4, name="Problem 2",
                 description="Another issue"
                )

session.add(menuItem2)
session.commit()


menuItem3 = Item(user_id=1, category=category4, name="Problem 3",
                 description="Another issue"
                )

session.add(menuItem3)
session.commit()

category5 = Category(user_id=1, name="Hashing",
                       description=
                        """Hashing is generating a value or values from a string
                        of text using a mathematical function.
                        """
                      )
session.add(category5)
session.commit()

menuItem1 = Item(user_id=1, category=category5, name="Problem 1",
                 description="Another issue"
                )

session.add(menuItem1)
session.commit()


menuItem2 = Item(user_id=1, category=category5, name="Problem 2",
                 description="Another issue"
                )

session.add(menuItem2)
session.commit()


menuItem3 = Item(user_id=1, category=category5, name="Problem 3",
                 description="Another issue"
                )

session.add(menuItem3)
session.commit()


print "added menu items!"
