"""
Script Name: IDMC_SA_Monitoring.py
Description:
   This script is used to send email alerts based on the monitoring of Secure Agent services. It reads configuration settings (such as SMTP server,sender/receiver emails, and encrypted credentials) from an external
   properties file. It decrypts the stored encrypted password using the Fernet symmetric encryption provided by the `cryptography` library.

Main Components:
   - Loads configuration values using `configparser` from a 'config.properties' file.
   - Decrypts the  password using Fernet and a predefined encryption key.
   - Login to Informatica Rest API using the creds and fetch the corresponding Session ID.
   - Check the Agent Status after an interval which can be updated and alert the team in case any of the service results "Error","Failed" etc
   - Uses the `smtplib` and `email.message.EmailMessage` to construct and send alerts.
Modules Used:
   - configparser: For reading configuration files
   - smtplib: For sending emails
   - email.message: For constructing email content
   - cryptography.fernet: For secure encryption/decryption of credentials
   - time: For potential timestamping or delay logic
Functions:
   - decrypt_password()
   - get_session_id()
   - send_alert(subject)
   - get_agent_status()

Script Usage:
   Before running this script make sure to update the config.ini file by updating the below fields
   - username
   - encrypted_password :- To get the below two field attributes , run encode_text.py which is meant to be run once and post that it will generate a key and the corresponding encrypted password. Copy both the values  encrypted_password and encrypted_key
   - encryption_key
   - agent_id :- To fetch the agent_id run the API https://emc1.dm1-em.informaticacloud.com/saas/api/v2/agent/ , and copy the id 
   
   Then run the script as a standalone monitoring alert or integrate it as a module. There is no need to schedule this script , as the script need to be run once and will run for ever. 

Author: Anshuj Verma
Date: 23 Jun 2025
"""

import json
import requests
import time
import json
import socket
import smtplib
from email.message import EmailMessage
from cryptography.fernet import Fernet
import configparser


#host
host_name=socket.gethostname()

#body
email_body = """\
Hi Team,
This is to notify you that a disruption has been detected in the Secure Agent services on the server.
Please review the Secure Agent status and take the necessary action to restore normal operations.
Regards,  
IDMC Platform 
"""

# Base URL of IICS
base_url = "https://dm1-em.informaticacloud.com/saas/public/core/v3"

# Load config
config = configparser.ConfigParser()
config.read('config.ini')
user=config['DEFAULT']['username']
server_url=config['DEFAULT']['server_url']
agent_id=config['DEFAULT']['agent_id']

# Login Path
login_path = '/login'
# All Connections Path

headers = {"Content-Type": "application/json", "Accept": "application/json"}


#Decode Password
def decrypt_password(encrypted_password, encryption_key):
    fernet = Fernet(encryption_key.encode())
    return fernet.decrypt(encrypted_password.encode()).decode()


# Get session ID
def get_session_id():

    creds = {"username": user, "password": decrypt_password(config['DEFAULT']['encrypted_password'],config['DEFAULT']['encryption_key'])}
    result = requests.post(url=base_url + login_path,
                       headers=headers, data=json.dumps(creds))

    if result.status_code == 200:
        #print(f"Login Successful, you are logged in as {user}")    
        return result.json()['userInfo']['sessionId']
    else:
        raise Exception(f"Login failed: {result.text}")

#Send Email Alert
'''
def send_alert(subject,name):
    org="UCB-SBX"
    msg=EmailMessage()
    msg['Subject']=subject
    msg['From']='Anshuj.Verma@ucb.com'
    msg['To']=config['SMTP']['email_recipients']
    email_body = f"""\
Hi Team,

This is to notify you that there have been service disruption detected on the Secure Agent {host_name} for the service {name}.
    
Please review the Secure Agent status on {org} ORG and take the necessary action to restore normal operations.
                            
Regards,  
IDMC Platform 
    """
    msg.set_content(email_body)
    with smtplib.SMTP(config['SMTP']['smtp_server'], 25) as smtp:
        smtp.send_message(msg)
'''
# Get agent status
def get_agent_status():
    ag_url = f"{server_url}/api/v2/agent/details/{agent_id}"
    response = requests.get(url=ag_url, headers=headers)
    data=response.json()
    
    if response.status_code == 200:
        #print("Entering into if clause")
        raw_data=data["agentEngines"]
        nm=[ c["agentEngineStatus"]["appname"] for c in raw_data]
        statuses=[ d["agentEngineStatus"]["status"] for d in raw_data ]
        #print(statuses)
        result_lst=list(zip(nm,statuses))
        not_running=[]
        for name,status in result_lst:
            if status != "RUNNING" :
                not_running.append((name,status))
            #     nm=name
            #     st=status
            # return nm,st
        if not_running:
            return not_running
        else:
            return "Running"

       

        
    # return "RUNNING"



# Main loop
if __name__ == "__main__":
    prev_status = "RUNNING"
    session_id = get_session_id()

    
    headers['INFA-SESSION-ID'] = session_id
    headers['icSessionId'] = session_id
    interval = 10

    while True:
        try:
            status =get_agent_status()
            print(status)
            # if isinstance(ct_status,tuple):
            #     name,current_status=ct_status
            if isinstance(status,list):
                for name,ct_status in status:
                    current_status=ct_status
                    print(f"⚠Secure Agent status changed from RUNNING to {current_status} for the service {name}")
            else:
                #print("The value of current status now when all service are ok ")
                current_status="RUNNING"
                
            #print(current_status)
            #if prev_status == "RUNNING" and current_status != "RUNNING":
            # if current_status != "RUNNING":
            #     print(f"⚠Secure Agent status changed from RUNNING to {current_status} for the service {name}")
                
                # send_alert(f"Secure Agent Service Alert from {host_name} -->>Action Required",name)
            prev_status = current_status
        except Exception as e:
            #print(f"Error: {e}")
            session_id = get_session_id()  # Retry session fetch
        time.sleep(interval)
      
