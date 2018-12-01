## Front-End To-Dos

In ```menu_choose_items.html```: 	

* Use Flask/Jinja2 to get all products, separated by category_id. Each product button has a unique ID and can be made of a class that identifies it as a particular category. 
  * DONE! --CSM
* Write javascript/d3 code that handles selections for each category, graying out everything in a category once an item has been selected, adding the item to a javascript object for submission. Submission happens when customer clicks on 'go to checkout'. I they haven't made a selection, we ignore their click.
  * Partially done. Upon click in a category the "Add Item" text disappears from the remaining category items.  --CSM
  * Data is spit out in a console log; however, still working on capturing it into the container that will be sent to the server and moved to the checkout.html page --CSM
* We probably don't want to use a regular form for this, but have d3/jquery handle the submission by using POST and sending a json to a flask API endpoint.
  * Need TA help .. this is where I will start on Saturday class. --CSM

```checkout.html```:

* This file has not yet been adjusted to work with our flask environment. Christian will do this Wednesday (11/28) morning.
  * Did this happen? I put content (or something) there, yet the page is broken and I'm unclear on the issue. I thought the code for the "Go To Checkout" button was correct, but seeing the d3/jquery POST thing, this may be something else. --CSM
* Flask will pass in recommendation that needs to be parsed by javascript (or jinja2 templating language) to provide recommendations.

