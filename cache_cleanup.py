from datetime import datetime, timedelta
import os
from pydoc import plain
import time
import logging
import socket
import smtplib
from email.message import EmailMessage
import configparser
from email.mime.text import MIMEText
host_name=socket.gethostname()
timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
config = configparser.ConfigParser()
config.read('config.ini')

class CacheCleaner:
    def __init__(self,cache_dir,days_threshold,f_path):
        self.cache_dir=cache_dir
        self.days_threshold=days_threshold
        self.f_path=f_path
        self.setup_logging()

    def setup_logging(self):
        
        log_dir=os.path.join(self.f_path,"Cache_logs")
        
        os.makedirs(log_dir,exist_ok=True)
        f_name=f"cache_cleanup_{timestamp}.log"
        log_file=os.path.join(log_dir,f_name)
        logging.basicConfig(
            level=logging.INFO,
            format="{asctime} - {levelname} - {message}",
            style="{",
            filename=log_file
        )
    


    def get_old_files(self):
        
        cut_off=datetime.now() - timedelta(days=self.days_threshold)
        #allowed_extension=['.tmp','.log','.dat','.idx']
        fl_lst=[]
        
        for filename in os.listdir(self.cache_dir):
            fl_lst.append(filename)

        
            
        files_old=[]   
        for file in fl_lst:
            file_path=os.path.join(self.cache_dir,file)
            mtime_seconds = os.path.getmtime(file_path)
            mtime_datetime = datetime.fromtimestamp(mtime_seconds)
            ext=os.path.splitext(file_path)[1]
            if ext.startswith('.dat') or ext.startswith('.idx') and mtime_datetime < cut_off:
                files_old.append(file)
            
                

        return files_old


    def clean_cache(self,old_files):
        count=len(old_files)
        
        if count == 0:

            email_body = f"Hi Team,\n\nThere are no Old Cache Files older than {self.days_threshold} days and hence the alert can be ignored"
            msg = MIMEText(email_body)
            msg['Subject']=f"Cache File Cleanup from {host_name}"
            msg['From']='Anshuj.Verma@ucb.com'
            msg['To']=config['SMTP']['email_recipients']
            with smtplib.SMTP(config['SMTP']['smtp_server'], 25) as smtp:
                smtp.send_message(msg)
                print("Email Sent successfully")
                

        else:
            
            email_body = f"Hi Team,\n\nFollowing are the files that are older than {self.days_threshold} and have been deleted :\n\n" + "\n".join(old_files)

            msg = MIMEText(email_body)
            msg['Subject']=f"Cache File Cleanup from {host_name}"
            msg['From']='Anshuj.Verma@ucb.com'
            msg['To']=config['SMTP']['email_recipients']

            with smtplib.SMTP(config['SMTP']['smtp_server'], 25) as smtp:
                smtp.send_message(msg)
                print("Email Sent successfully")
            
            

            file_path=self.cache_dir
            #print(file_path)

            for file_to_delete in old_files:
                cache_file_path=os.path.join(file_path,file_to_delete)
                os.remove(cache_file_path)
                #print(cache_file_path)

            #for old in old_files:
                #os.remove(old)
            
            

            '''
            for old in old_files:
                try:
                    os.remove(old)
                    #logging.info(f"Removed: {old}")
                except Exception as e:
                    #logging.error(f"Failed to remove {old}: {str(e)}")
            

            msg.set_content(email_body)
            with smtplib.SMTP(config['SMTP']['smtp_server'], 25) as smtp:
                smtp.send_message(msg)

            '''



    

if __name__=='__main__' :
    cleaner=CacheCleaner((r"D:\software\ICSA\apps\Data_Integration_Server\data\cache"),days_threshold=1,f_path=r"D:\software\platform")

    old_files=cleaner.get_old_files()
    print(f"Old Files are {old_files}")
    
    cleaner.clean_cache(old_files)
    



