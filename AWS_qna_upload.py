import boto3
from uuid import uuid4

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')   # Replace 'your_region_name' with your AWS region
table=dynamodb.Table('QA_testing')
 

db=[]
for line in db:
     line['id'] = uuid4().hex
     table.put_item(Item=line)


#print(db)
#data2 =Question.get_item(Key={'id':"5df4g6ad4g64g64fdga4dfg4adf"})
# response = table.scan()
# result = response['Items']
# print(result)
# line =  {'question': "What's your favorite way to unwind after a long day?", 'answer': "Answering to question What's your favorite way to unwind after a long day?", 'attributes': ['favorite', 'way', 'unwind', 'long day'], 'synonyms': ['preferred', 'method', 'relax', 'extended day'], 'id': '24e80121fe6f4ca2b0cc21222a2f24ef'}



# [
#                 {'question': "What's your favorite way to unwind after a long day?", 'answer': "Answering to question What's your favorite way to unwind after a long day?", 'attributes': ['favorite', 'way', 'unwind', 'long day'], 'synonyms': ['preferred', 'method', 'relax', 'extended day'], 'id': '24e80121fe6f4ca2b0cc21222a2f24ef'},
#             {'question': 'If you could travel anywhere in the world right now, where would you go?', 'answer': 'Answering to question If you could travel anywhere in the world right now, where would you go?', 'attributes': ['travel', 'anywhere', 'world', 'right now', 'go'], 'synonyms': ['journey', 'everywhere', 'globe', 'immediately', 'proceed'], 'id': '3e34ca8d3feb443e89bffe723df28a96'}
#             ]





# [{"question":"what is edyou","answer":"sldkjpsdkkgk;mgkgsgkfngkGDf","Attributes":["attr1","attr2"],"Synonyms":[]}]











