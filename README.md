Step 1:- create a folder in your system kafka in this folder create a file docker-compose.yml 

Step 2:- docker-compose up -d

Step 3:- python manage.py runserver

Step 4:- python manage.py kafka_consumer

``` in kafka_consumer we have created a custom command which run kafka consumer ```

Step 5:- type locust on terminal it eill open on port http://0.0.0.0:8089

number of user:- 10 request will be send to user.

ramp up:- 1 # in  every 1 sec 10 user will send the request.



1)In this project we have created a like counter where when we send 1000 of request and update like on post without kafka db crashes and db is locked so to overcome this problem 
we have used kafka.

2)Here we have created a model post which store title and like.

3)we have created a views with function <h1>post_like</h1> .

4)after that it calls for <h1>send_like_event(post_id)</h1>.

5)this is a function part of kafka_producer.py which will act as kafka producer.

6)we will also run python manage.py kafka_consumer which will consume the data and store in db.