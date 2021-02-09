# Twitter-Like-Clone
This project involves creating microservices to produce functionality of a Twitter-Like message system. It is written as a separate Flask framework application under RESTful API attributes. It includes database technologies such as SQL(SQLite) and NoSQL(DynamoDB) to store user messages and their timeline feeds. Additionally, the server side associates with a API Gateway, load-balancing, and authenication. 

Services Used:
		1. DynamoDB local
		2. SQLite
		3. Flask 
		4. Boto3
		5. httpie 

How to dynamodb table is created:
	***The dynamodb table is created from a separate py file called "create_table.py", the python file includes the schema used to initialized the database.
	Additionally, the table is then populated with test data by the use of a json file called "test-load.json".***
	
	1. Open terminal and navigate to the project folder
	2. flask init //To initialize and populate the dynamodb table

How to run:
	**Before running, check if dynamodb table is created yet. If not, follow the create dynamodb step above**
	1. Open terminal and navigate to project folder
	2. type in cmd "export FLASK_APP=api_users.py"
	3. flask init //To create the database table of users/timeline services and populate it
	4. Run "java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb"
	5. Open another terminal in project folder and run "foreman start -m gateway=1,auth=1,api_users=3,api_timeline=3,app=1"

Authenication: 
	To authorize login:
	http -a USERNAME:PASSWORD POST localhost:5000/login username=USERNAME password=PASSWORD
	
	Example with our microservices:
	http -a mj:bulls POST localhost:5000/login username=mj password=bulls


Example Calls:
> http -a mj:bulls POST localhost:5000/sendmsg to=kobe from=jordan msg=testing

> http -a mj:bulls POST localhost:5000/replyto to=jordan from=kobe msg=hello reply-to-id=24

**quick replies by providing index**
> http -a mj:bulls POST localhost:5000/replyto to=kobebryant from=mj quick-reply=2

> http -a mj:bulls GET localhost:5000/listreplies/24

> http -a mj:bulls GET localhost:5000/listmsg/kobebryant
