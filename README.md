# moneyManager

Goals:
===================================================

modelBlender: 
* From a collection of orders and its outcomes produce an strategy that 'minimizes risk'. 
* Carefully backtest each model independently and the joint model
* Produces a blended model {'model1':0.0, 'model2':0.3, 'model3':0.4, 'model4':0.3} with its performance

dataGathering: 
* get csv files of as many stocks as possible, frequency=1sec

basicModeling: 
* Systematically produces and evaluates very simple strategies. 
* Sample strategy: if stock pases some threshold we should buy and keep until something else happens.



## Questions to Jake:
* Data provider (currently using sample (adjusted) data from Kibot): he uses polygon
* How can I authomatize making orders, is there an api? how does this even work in real life? he mentioned 'efficient frontier'
* Cost per order (0.5 cents per share or 2 dollars per trade)
* Latency issues to be aware of.
* How/at what point can we know if we are `moving the market` too much? In the afternoon there is very little volume.


## Notes from Jake
* Tick data might be more useful for quant analysis.
* polygon.io source of data.
* thinkorswim.com: 2 dollars per trade, 
* interactivebrokers : half a cent per share.
* kelly criterion?
* ibridgepy ... take quantopian to real life.
* zipline - quantopian type of thing.
* efficient frontier. for blending the strategies.
* kygo: his thing.
* Use quantopian!





