import fun_decrypt as fd
import requests
import json
import pandas as pd

# Base URL of IICS
baseurl = "https://dm-us.informaticacloud.com/saas/public/core/v3"
# Login Path
login_path = '/login'

#User API
user_data='/public/core/v3/users'

# Logoff path
logoff_path = '/logout'

headers={"Content-Type":"application/json","Accept":"application/json"}

result= requests.post(url=baseurl + login_path,headers=headers,data=json.dumps({'username':fd.usr,'password':fd.pwd}))

session_Id=result.json()['userInfo']['sessionId']

if session_Id:
    headers['icSessionId']=session_Id
    headers['INFA-SESSION-ID']=session_Id

else:
    exit()

base_url=result.json()['products']
base_api_url=[ d.get('baseApiUrl') for d in base_url ]
base_url_lst_str = ' '.join(map(str, base_api_url))

user_api=base_url_lst_str+user_data
limit_val=200
skip_val=0
all_name=list([])
all_f_name=list([])
all_l_name=list([])
all_status=list([])
all_email=list([])
all_group=list([])

while True:
    # print(f"when the value os n is {n}")
    user_api_limit=f'{user_api}{"?limit="}{limit_val}{"&skip="}{skip_val}'
    print(user_api_limit)

    res=requests.get(url=user_api_limit,headers=headers)
    res_data=res.json()
    if len(res_data) == 0:
        break
    else:
        # print(res_data)
        skip_val+=200
        name=[ d.get('userName',None) for d in res_data]
        all_name.append(name)
        f_name=[ d.get('firstName') for d in res_data]
        all_f_name.append(f_name)
        l_name=[ d.get('lastName') for d in res_data]
        all_l_name.append(l_name)
        status=[ d.get('state') for d in res_data ]
        all_status.append(status)
        email=[ d.get('email',None) for d in res_data ]
        all_email.append(email)
        group= [','.join([i['userGroupName'] for i in d['groups']]) for d in res_data]
        all_group.append(group)

all_name_lst=[]
for row in all_name:
    all_name_lst+=row

print(all_name_lst)

f_name_lst=[]
for row in all_f_name:
    f_name_lst+=row

l_name_lst=[]
for row in all_l_name:
    l_name_lst+=row

status_lst=[]
for row in all_status:
    status_lst+=row

email_lst=[]
for row in all_email:
    email_lst+=row

group_lst=[]
for row in all_group:
    group_lst+=row



dict={'Name':all_name_lst,'FirstName':f_name_lst,'LastName':l_name_lst,'Email':email_lst,'Status':status_lst,'UserGroup':group_lst}

df = pd.DataFrame(dict) 
df.to_csv("UserDetails_so002_Dev.csv", index=False) #using to_csv() 

result = requests.post(url=baseurl + logoff_path, headers=headers)
print("Successfully close the session.")
