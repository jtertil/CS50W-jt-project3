## CS50W2019 Project 3 [Work in progress]

### About:
This is ongoing project. I will build an web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

#### Technologies used:
 * Python 3: Django 2.2, [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar), [django-redis](https://niwinz.github.io/django-redis/latest/)
 * PostgreSQL 10, Redis
 * Unittest, Coverage
 * JavaScript, Bootstrap, jQuery,


### Project milestones:
- [x] Complete the Menu, Adding Items, and Registration/Login/Logout steps.
- [ ] Complete the Shopping Cart and Placing an Order steps.
- [ ] Complete the Viewing Orders and Personal Touch steps.


### Project requirements:
- [x] Menu: Your web application should support all of the available menu items for [Pinnochio’s Pizza & Subs](http://www.pinocchiospizza.net/menu.html) (a popular pizza place in Cambridge). It’s up to you, based on analyzing the menu and the various types of possible ordered items (small vs. large, toppings, additions, etc.) to decide how to construct your models to best represent the information. Add your models to orders/models.py, make the necessary migration files, and apply those migrations.
- [x] Adding Items: Using Django Admin, site administrators (restaurant owners) should be able to add, update, and remove items on the menu. Add all of the items from the Pinnochio’s menu into your database using either the Admin UI or by running Python commands in Django’s shell.
- [x] Registration, Login, Logout: Site users (customers) should be able to register for your web application with a username, password, first name, last name, and email address. Customers should then be able to log in and log out of your website.
- [x] Shopping Cart: Once logged in, users should see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their virtual “shopping cart.” The contents of the shopping should be saved even if a user closes the window, or logs out and logs back in again.
- [ ] Placing an Order: Once there is at least one item in a user’s shopping cart, they should be able to place an order, whereby the user is asked to confirm the items in the shopping cart, and the total (no need to worry about tax!) before placing an order.
- [ ] Viewing Orders: Site administrators should have access to a page where they can view any orders that have already been placed.
- [ ] Personal Touch: Add at least one additional feature of your choosing to the web application. Possibilities include: allowing site administrators to mark orders as complete and allowing users to see the status of their pending or completed orders, integrating with the Stripe API to allow users to actually use a credit card to make a purchase during checkout, or supporting sending users a confirmation email once their purchase is complete. If you need to use any credentials (like passwords or API credentials) for your personal touch, be sure not to store any credentials in your source code, better to use environment variables!


### How it works:
It doesn't work at this time. But I'll take care of it ASAP. :)

### How it looks: 
No front-end at this stage. But I got an idea that it should be somewhat closer to this: 
![vespa scooters](https://d39a3h63xew422.cloudfront.net/wp-content/uploads/2016/02/21034229/is-this-piaggio-museum-the-most-cheerful-place-in-italy-1476934523082-2000x1331.jpg) 

rather than this: 
![pakistan bus](https://i.ytimg.com/vi/v1uQP40wg7w/maxresdefault.jpg) 

:)