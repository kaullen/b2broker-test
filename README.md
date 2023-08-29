# b2broker-test

## Motivation
The most controversial decision I've made in this project is storing wallet balance in a DB field insted of calculating it on the fly.
The other possible solution was to aggregate all the wallet's transactions and sum them whenever we need to return a balance. My reasoning for implementing the first approach is as follows:

* **Time considerations:** a wallet can potentially have millions of transactions. 
If we calculate the belence every time then as the number of transactions grows, the "get balance" query execution time will grow linearly with it. 
That raises the DB load as well as API response time, so this approach can potentially cause problems.
With the statically stored balance, this problem doesn't exist: retrieving it will take a constant amount of time every time regardless of the number of transactions.

* **Redundancy:** when the data is stored in two separate places, it will be much easier to restore in case the database gets partially corrupted.

* **Fun:** given how this is a test task with no real-world implications I decided to just go with the path that was more interesting to write :)

Arguments for the aggregate approach include:

* **Time considerations:** while balance retrieval, as mentioned above, grows with the number of transactions, the process of transaction creation doesn't require any additional actions and is executed in a single query (as opposed to two).
This increase also slightly grows with the number of wallets and transactions in the database, given how we heed to retrieve previous values when we save a new one.
However, this growth is much, much slower (since we're using index colums, it's only logarythmical), and also one can reasonably expect balance retrieval to be much more common than transaction creation, so this is a minor issue.

* **Data security:** the logic for balance recalculation is currently contained entirely within Django's model framework. 
This means that by accessing the DB through anything other than this API it is possible to modify certain values so that they are no longer matching and such a modification would be very hard to track.
This can be semi-bypassed by something like CRON/Celery task that would regularly validate all the balances, although this would put a bit of an extra load on the DB.
Also, the logic can be entirely moved into the DB as some kind of macros, which will alleviate at least some of the problems.

* **Ease of further development:** in its current form, the logic only works when transactions are saved and processed one-by-one via directly or indirectly calling the transaction model's `.save()` or `.delete()` method.
This works fine with how Django Rest Framework operates and how API requests are handled; however, if at some point there arises a need to somehow ineract with transactions programmatically inside the code, one should always keep this limitation in mind.
An example of a common situation where this explicitly wouldn't work is modifying/deleting transactions via queryset methods, whether in bulk or one-by-one.
This can be easily rectified by implementing custom queryset/manager classes, but at some point the code's bound to become too cumbersome to support.

A potentially optimal approach would be to implement the dynamic aggregation strategy but cache the results in a non-persistent storage in order to avoid constant recalculation. However, this would cause other issues such as having to decide what kind of lag is acceptable when retrieving the balance.
