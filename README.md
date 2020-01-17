January 15:
===================================================
* The notebook used to define the target is quite cool, still we need to add to start counting the number of transactions we are doing
* Also in the same notebook: our strategy requires to hold a position until there is a better signal, we need to include this in the simulations.
* Today: focus on creating the target ! a final one!



January 13/2020:
===================================================
Notes:
-------------
* Move to python 3.5
* Careful! Our target is wrong, we need to compute the quotient-time series (not difference ... that is what matters.)
* Start reading/implementing things on quantopian: focus on data gathering: (method loadTimeSeries())
* Have the pipeline and the current notion of target implemented
* See how good is the precision recall curve we can get with Logistic regression and (maybe) random forests
* If the precision and recall are 'reasonable' proceed to wrap the pipeline into an object StockModel that produces all the statistics we need.


Note from Dan Whitnable (quantopian) (what is ziplane?)
-------------
Quantopian does not provide support for installing or running local installations of zipline. We only support the online Quantopian platform. Perhaps take a look at this post https://www.quantopian.com/posts/guide-for-porting-your-algorithms-to-a-local-zipline-research-environment which may offer some help. You are also welcome to post in the forums to request help from the community.

Note from Juraij (former DRW)
---------------
Question: hey, do you have any resource that you recommend to read about strategies used nowadays?
Unfortunately, I don't know the literature on this well. At my company we weren't really reading books on this topic. I guess the best advice is to come up with some "signal" (some value that you believe should be predictive of something), and then look how your target depends on this signal, and then try to improve it. In the end, if you have a couple of (at least somewhat independent) signals, you combine them in some way to get a final predictor (e.g. linear regression, logistic regression, boosted trees (which have become quite popular, from what I heard)). Typical themes of signals would be: movement of your stock relative to movement of correlated stocks, book dynamics, price momentum, ... However, I don't have much experience with time horizons longer than 1-2 minutes so I am not sure how useful I could be.

and those signals typically come from the time series/tick data itself or is it a huge chunk of external data

Question: and those signals typically come from the time series/tick data itself or is it a huge chunk of external data?
A "signal" is whatever you come up with that has some (hopefully not spurious) correlation with your target (typically some price movement). You could create it just from time series of prices, or from any other data. In our group, the data we were using was tick data, meaning we had access to the whole state of the marketplace and all the "atomic" changes that are happening through a trading day. From that you can extract various signals that could be based on current state of the book, recent price changes, ...
If you want to predict on long time scales (like several months), then fundamentals (net income, debt level, sales growth, ...) can be very important. Long time scales are tricky, however, since you have much smaller number of (uncorrelated) data points. 
I also heard options positioning can be informative at times.

January 10/2020: (improvement in target definition and finding minimal performance requirements for our models)
===================================================
* Created a notebook with the goal of defining a target, results are very promising.
* The main takeouts are the following, if we only trade two stocks (IBM, IOH) and we are able to guess every minute which of the stocks is going to 'perform better'
The next minute with precision of around 80% (maybe a bit more) and recall of 5% (maybe a bit less) we would be able to beat the market in a sustainable way.


January 7/2020: (Cool idea: trade pairs of stocks and predict which stock is going to 'perform better' the next minute)
===================================================
* Given that all we want to do at the end is operations of the type (sell/buy), We could, for instance, model stocks by pairs. In this scenario, a very natural target appears precisely
When the value of one of the stocks increases more than the other: this would clearly
Suggest a (buy/sell), and again, we can keep modeling this as a classification.
* Modeling/predicting a target is not enough. Test asap if we can actually make money from the target we are predicting.


January 4/2020
=====================================================
* Models are apparently ok the baseline is definitely improved.
* Lets start turning them into a deployable strategy, maybe try to get alpha on top of DowJones?
* We could encode time way better in the pipeline
* Remember adding the differences of the time series to the pipeline
* Need a more elaborated way of looking at histograms: the tails don't let me see anything: those tails are a huge concern.
* Look out for sklearn methods to do cross validation in our setting: do not reinvent the wheel.


December 30/2019: Notes from conversation with Jake
=====================================================
* Data provider (currently using sample (adjusted) data from Kibot): he uses polygon
* How can I authomatize making orders, is there an api? how does this even work in real life? he mentioned 'efficient frontier'
* Cost per order (0.5 cents per share or 2 dollars per trade)
* Latency issues to be aware of.
* How/at what point can we know if we are `moving the market` too much? In the afternoon there is very little volume.
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


December 30/2019
=====================================================
* We will need one day to Plot a precision recall curve with several(monthly/weekly) training batches


December 29/2019
=====================================================
* The distribution of the difference of the time series has very long tails: see plot. This was expected; still very ugly.
* Created a very clean dataset with 'pastValues', 'currentValue', 'futureValue', 'deltaMinutes'. 
* The precision recall curve that we already have looks quite good: we trained one single time.


December 26 - Goals:
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


## Notes about the idea of a model blender:
* What is an order? Focus on one type of order
* What is an outcome? differentiate between real outcome and simulated outcome.
* What is a blended model?
- input: available cash, order, time until markets close (?), max_transaction limit
- output: authorization/non-authorization to execute the order.

* Type of order: buy one unit
 Stock: MSFT
 Start time: 1:00pm
 Expiration time at 1:05pm. 
 Initial buy at 11 USD 
 Keep interval: [10, 15] (if goes below 10 or above 15: sell)
 [if MSFT goes bellow]
