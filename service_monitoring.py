import json 
import requests
import pandas as pd

# Base URL of IICS
base_url = "https://dm1-em.informaticacloud.com/saas/public/core/v3"
# Login Path
login_path = '/login'

#Runtime Path
runtime_path='/api/v2/runtimeEnvironment'
#Agent Path
agent_path='/api/v2/agent'
#Agent Details Path
agent_details_path='/api/v2/agent/details'

# Logoff path
logoff_path = '/logout'

headers={"Content-Type":"application/json","Accept":"application/json"}
# request_header = {'Accept': 'application/json', 'Content-Type': 'application/json'}

with open(r"C:\Users\2109382\OneDrive - Cognizant\Documents\Python_Restart\Infa\config_ucb_sbx.json",'r') as f:
    config=json.load(f)
    user=config['username']
    pwd=config['password']

creds={"username":user,"password":pwd}
result= requests.post(url=base_url + login_path,headers=headers,data=json.dumps(creds))


session_Id=result.json()['userInfo']['sessionId']


if session_Id:
    headers['INFA-SESSION-ID']=session_Id
    headers['icSessionId']=session_Id
    print(session_Id)
else:
    exit()

base_API_Url=result.json()['products']
res=[d.get('baseApiUrl',None) for d in base_API_Url]
base_url_lst_str = ' '.join(map(str, res))   #Base Url
agent_url=base_url_lst_str + agent_details_path

agent_details=requests.get(url=agent_url,headers=headers)
service_lst=[]
agent_data=agent_details.json()
# agent_resp=dict(agent_data)
agent_resp={}    #Convert the list into dictionary 
for i in agent_data:
    agent_resp.update(i)
    
print(agent_resp)    
print(type(agent_resp))

print(agent_resp.get('agentEngines',{}.get('agentEngineStatus',{}.get('appDisplayName'))))
# svc_name = list([])     #Contain Secure Agent Name 
# for item in agent_resp:
#     # try:
#         print(item.get('agentEngines',{})[0]['appDisplayName'])
#         svc_name.append(item.get('agentEngines',{})[0]['appDisplayName'])
    # except (AttributeError, IndexError) as e:
    #     print("No Service found")
    #     svc_name.append('NA')

# print(svc_name)
# ser_lst=agent_resp.get('agentEngines',{}.get('appname'))
# serv2=agent_resp['agentEngines']['agentEngineStatus']
# services = agent_resp.get('agentEngines', {}).get('appDisplayName', [])
# ser_lst=[d.get('agentEngines',{}.get('appname'))for d in agent_resp ]
# print(services)
# agent_name=[d.get('name',None)  for d in agent_data]
# print(agent_name)
# agent_status=[d.get('active',None)  for d in agent_data]
# print(agent_status)
# service_lst=[d.get('agentEngines',{}).get('appDisplayName',[]) for d in agent_data]
# print(service_lst)

# services=agent_data.get('agentEngines', {}).get('appname', [])




