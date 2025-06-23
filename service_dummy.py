
def service_check():

    statuses=["RUNNING","RUNNING","FAILED"]

    for status in statuses:
        if status != "RUNNING":
            return status

        
    return "RUNNING"

sc=service_check()
print(sc)
if sc == "RUNNING":
    print(f"All the services are currently up and running {sc}")
else:
    print("Not All services are up , please take required action")