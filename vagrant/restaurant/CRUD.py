# In this lesson, we performed all of our CRUD operations with SQLAlchemy
# on an SQLite database. Before we perform any operations, we must first
# import the necessary libraries, connect to our restaurantMenu.db, and
# create a session to interface with the database:


# http://docs.sqlalchemy.org/en/rel_0_9/orm/query.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


############################
# CREATE entry in database #
############################

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarela", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()


############################
# READ (or query) database #
############################

session.query(myFirstRestaurant).all()
# Will return something like:
# [<database_setup.Restaurant object at {someplace in memory}>]

# query single row
firstResult = session.query(Restaurant).first()
firstResult.name
# u'Pizza Palace'

items = session.query(MenuItem).all()

for item in items:
    print item.name
# returns all names for table MenuItem


#########################
# UPDATE database entry #
#########################

# In order to update and existing entry in our database, we must execute the following commands:
#
#     1. Find Entry
#     2. Reset value(s)
#     3. Add to session
#     4. Execute session.commit()


veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()
print UrbanVeggieBurger.price
# $5.99

UrbanVeggieBurger.price = "$2.99"
session.add(UrbanVeggieBurger)
session.commit()

for veggieBurger in veggieBurgers:
    if veggieBurger.price != "$2.99":
        veggieBurger.price = "$2.99"
        session.add(veggieBurger)
        session.commit()

# Rerunning prevous for loop shows all veggieBurgers are now $2.99


#########################
# DELETE database entry #
#########################

# To delete an item from our database we must follow the following steps:
#
#     1. Find the entry
#     2. Session.delete(Entry)
#     3. Session.commit()


spinach = session.query(MenuItem).filter_by(name ="Spinach Ice Cream").one()
print spinach.restaurant.name
# 'Auntie Ann's Diner'
session.delete(spinach)
session.commit()
# Running spinach = session... returns 'NoResultFound("No row was found for one()")'
