#Project 5 - Create table of Dynamodb
import boto3


def directmsg(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='directmsg_user',
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'fromUser',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'fromUser',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'textID',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10,
        },
        GlobalSecondaryIndexes= [ 
            { 
       
		        'IndexName': 'text_index', 
		        'KeySchema': [
		            { 
		                'AttributeName': 'textID',
		                'KeyType': 'HASH',
		            }
		        ],
		        'Projection': { 
		            'ProjectionType': 'ALL' 
		        },
		        'ProvisionedThroughput': { 
		            'ReadCapacityUnits': 10,
		            'WriteCapacityUnits': 10,
		        },
        
            }
        ]
        

    )
    return table


#if __name__ == '__main__':
#    movie_table = directmsg()
#    print("Table status:", movie_table.table_status)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              #Project 5 - Create table of Dynamodb
import boto3


def directmsg(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='directmsg_user',
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'fromUser',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'fromUser',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'textID',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10,
        },
        GlobalSecondaryIndexes= [ 
            { 
       
		        'IndexName': 'text_index', 
		        'KeySchema': [
		            { 
		                'AttributeName': 'textID',
		                'KeyType': 'HASH',
		            }
		        ],
		        'Projection': { 
		            'ProjectionType': 'ALL' 
		        },
		        'ProvisionedThroughput': { 
		            'ReadCapacityUnits': 10,
		            'WriteCapacityUnits': 10,
		        },
        
            }
        ]
        

    )
    return table


#if __name__ == '__main__':
#    movie_table = directmsg()
#    print("Table status:", movie_table.table_status)
