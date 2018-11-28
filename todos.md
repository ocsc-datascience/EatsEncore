## Front-End To-Dos

In ```menu_choose_items.html```: 	
 
* Use d3 or jquery/ajax to query get_products/1 endpoint and get all products. Use d3 to add and display items logically arranged by category.

* Write javascript/d3 code that handles selections for each category, graying out everything in a category once an item has been selected, adding the item to a javascript object for submission. Submission happens when customer clicks on 'go to checkout'. I they haven't made a selection, we ignore their click.

* We probably don't want to use a regular form for this, but have d3/jquery handle the submission by using POST and sending a json to a flask API endpoint.


```checkout.html```:

* This file has not yet been adjusted to work with our flask environment. Christian will do this Wednesday (11/28) morning.
* Flask will pass in recommendation that needs to be parsed by javascript (or jinja2 templating language) to provide recommendations.