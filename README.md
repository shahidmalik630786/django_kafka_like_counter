<h1>Kafka Like Counter</h1>

<h3>Step 1:- create a folder in your system kafka in this folder create a file docker-compose.yml </h3>

<h3>Step 2:- docker-compose up -d </h3>

<h3>Step 3:- python manage.py runserver</h3>

<h3>Step 4:- python manage.py kafka_consumer</h3>

<p>in kafka_consumer we have created a custom command which run kafka consumer </p>

<h3>Step 5:- type locust on terminal it eill open on port http://0.0.0.0:8089</h3>

<p>number of user:- 10 request will be send to user.</p>

<p>ramp up:- 1 # in  every 1 sec 10 user will send the request.</p>

<h2>Project Explanation</h2>

<p>1)In this project we have created a like counter where when we send 1000 of request and update like on post without kafka db crashes and db is locked so to overcome this problem 
we have used kafka.</p>

<p>2)Here we have created a model post which store title and like.</p>

<p>3)we have created a views with function <b>post_like</b>.</p>

<p>4)after that it calls for <b>send_like_event(post_id)</b>.</p>

<p>5)this is a function part of <b>kafka_producer.py</b> which will act as kafka producer.</p>

6)<p>we will also run <b>python manage.py kafka_consumer</b> which will consume the data and store in db.</p>

