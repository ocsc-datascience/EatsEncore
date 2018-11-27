# Notes on EatsEncore Machine Learning Engine

## Market Basket Analysis

Essentially, we're dealing with a market basket problem. Customer bought {1,2}, what is the most likely third item? {1,2} -> {3}?

The approach to this is to use the so-called [Apriori algorithm](https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/), which is a classical supervised-learning machine learning algorithm based. 

However, this is not supermarket basket analysis. We're doing this for restaurants/fast-food joints with item categories (based on the data):

* Side
* Desert
* Entree
* Kids
* Beverages
* Alcoholic Beverages

Some caveats:

* Some menu items come with a beverage.
* Many orders have more than one item per category because they were most likely for multiple people. Got to deal with this.
* Need to build adaptive recommendation engine. Customer selects entree -> predict beverage, side, dessert etc. Bev. in the following may include alcoholoic beverages.
	* {entree} -> {side,bev,dessert}
	* {entree,side} -> {bev,dessert}
	* {entree,side,dessert} -> {bev}
	* {entree,side,dessert,bev} -> {alc. bev}?
* Need to get user age:
	* offers of alc. beverage
	* offers of kids itesms
* Location 1: 58.6k items for lunch, only 9k dinner items. **Ignore Lunch/Dinner**? 	

### Assumptions/Restrictions/Scope Control

* Customers are individuals, party of one.
* Ignore Lunch/Dinner
* Use Age for alcohol and kids items
* User may choose 1 beverage/alc. beverage, 1 entree, 1 side, 1 desert (???)
  * Allowing them to choose more than one item per category will make the problem much much harder.
* Ignore multiple purchases of the same item.
* Ignore multiple purchases of the same category (???)

### Learning considerations

* Learn choices for other categories based on single item of one category? {burger} -> {beer}
* Also learn choices of other categories based on ensible of items from different categories. {burger,fries} -> {beer}
* What if user picks/edge cases: 
  * {side} -> {bev}?
  * {dessert} -> {bev}?
  * {bev/alc. bev} -> {dessert,side}?

### Issues

* How to separate train and test sets and how to compute loss?
* Is our category restriction making the problem too easy? We could lossen it and allow free prediction, e.g., {burger, veg. Chilli} -> {fries}.

### Some Useful Links

  * [https://towardsdatascience.com/use-algorithms-to-recommend-items-to-customers-in-python-347b769b21f3](https://towardsdatascience.com/use-algorithms-to-recommend-items-to-customers-in-python-347b769b21f3)
    Affinity score

  * May not be applicable here: [https://medium.com/datadriveninvestor/how-to-build-a-recommendation-system-for-purchase-data-step-by-step-d6d7a78800b6](https://medium.com/datadriveninvestor/how-to-build-a-recommendation-system-for-purchase-data-step-by-step-d6d7a78800b6)

  * A video on Market Basket Analysis
    [https://www.youtube.com/watch?v=ORxC8LcwVVE](https://www.youtube.com/watch?v=ORxC8LcwVVE)


  * [https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/](https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/)

  * [https://www.kaggle.com/datatheque/association-rules-mining-market-basket-analysis](https://www.kaggle.com/datatheque/association-rules-mining-market-basket-analysis)
  
  
