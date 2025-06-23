import json 
import requests
import pandas as pd

# Base URL of IICS
base_url = "https://dm-us.informaticacloud.com/saas/public/core/v3"
# Login Path
login_path = '/login'

#Runtime Path
runtime_path='/api/v2/runtimeEnvironment'
#Agent Path
agent_path='/api/v2/agent'

# Logoff path
logoff_path = '/logout'

headers={"Content-Type":"application/json","Accept":"application/json"}
# request_header = {'Accept': 'application/json', 'Content-Type': 'application/json'}

with open(r"C:\Users\2109382\OneDrive - Cognizant\Documents\Python_Restart\Infa\config.json",'r') as f:
    config=json.load(f)
    user=config['username']
    pwd=config['password']

creds={"username":user,"password":pwd}
result= requests.post(url=base_url + login_path,headers=headers,data=json.dumps(creds))


session_Id=result.json()['userInfo']['sessionId']

if session_Id:
    headers['INFA-SESSION-ID']=session_Id
    headers['icSessionId']=session_Id
else:
    exit()

base_API_Url=result.json()['products']
res=[d.get('baseApiUrl',None) for d in base_API_Url]
base_url_lst_str = ' '.join(map(str, res))   #Base Url
agent_url=base_url_lst_str + agent_path

agent_details=requests.get(url=agent_url,headers=headers)
# print(agent_details.json())

runtime_url=base_url_lst_str + runtime_path
runtime_details=requests.get(url=runtime_url,headers=headers)
runtime_data=runtime_details.json()

print(runtime_data)       #Contain the json for runtime agent group 

# for item in runtime_data:
#     if len(item['agents'])== 0:
#         print("No agent Found" )
#     else:
#         print(item['agents'])
# sa_agent_group=[ d.get('name',None) for d in runtime_data ]
# print(sa_agent_group)     #Contain Secure Agent Group 


#agent_name=d.get('emea-sa-aws-cloud-ag-001-sandbox',{} for d in runtime_data)
#print(agent_name)
# print(f"Length of runtime data is {len(runtime_data)}")

# print('************************')
#print(runtime_data)

# agent_name = list([])     #Contain Secure Agent Name 
# print(type(runtime_data))

all_records = list({})
for run_env in runtime_data:
    each_row= list([])
    # Get information from outer JSON
    each_row = [run_env['name'], run_env['createTime'], run_env['updateTime'], run_env['createdBy'], run_env['updatedBy']]
    if len(run_env['agents']) == 0: # In case no data
        agent_name_status = ['NA', 'NA']
        each_row += agent_name_status
        all_records.append(each_row)
    else:
        for agent in run_env['agents']:
            each_row = [run_env['name'], run_env['createTime'], run_env['updateTime'], run_env['createdBy'], run_env['updatedBy']]
            each_row += [agent['name'], agent['active']]
            all_records.append(each_row)
            print(f"Each row is {len(each_row)}")
            print(f"Each row is {each_row}")


df = pd.DataFrame(all_records, columns=['AgentGroup', 'createTime', 'updateTime', 'createdBy', 'updatedBy', 'agentName', 'agentStatus'])
print(df)
print(df.to_string())
df.to_csv('Runtime_Agent_Status_so002Dev.csv', index=False)
exit(0)

'''
for item in runtime_data:
    try:
        print(item.get('agents',{})[0]['name'])
        agent_name.append(item.get('agents',{})[0]['name'])
    except (AttributeError, IndexError) as e:
        print("No agent found")
        agent_name.append('NA')
    # print(runtime_data.get('agents',{})[0])

print(f"Agent names are {agent_name}")
print(agent_name)

index=0
runtime_status=[]       #Contain status for Secure Agent 
while(index < len(agent_name)):
    agent=agent_name[index]
    agent_status=f'https://usw1.dmr-us.informaticacloud.com/saas/api/v2/agent/name/{agent}'
    
    index+=1
    
    if agent=='NA':
        runtime_status.append('NA')
        continue

    else:
         ag_status=requests.get(url=agent_status,headers=headers)
         runtime_status.append(ag_status.json()['active'])


print(runtime_status)

dict={'Sa_Agent_Group':sa_agent_group,'Secure_Agent':agent_name,'Agent_Status':runtime_status}

df = pd.DataFrame(dict) 
df.to_csv("Secure_Agent_Status_SBX.csv", index=False)
    

# try:
#     ag_status=requests.get(url=agent_status,headers=headers)
#     print(ag_status.json())

# except(403):

#     print("None")

# print("========= End of Program ========")

# df_agents = pd.json_normalize(runtime_data)

# print(df_agents.head(10))
# print(df_agents.to_csv('agents_data.csv', index=False))
'''