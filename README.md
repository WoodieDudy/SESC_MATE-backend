Это бек для vk mini app SESC MATE https://vk.com/app7227055
Также сюда встроен бот вк для уведомлений об изменениях расписания


**INSTALLING**

`git clone https://github.com/S3K-studio/SESC_MATE-backend.git`  
`cd SESC_MATE-backend`  
`python3 -m venv venv`  
`pip install -r requirements.txt`  
`install redis on your machine`

**STARTING**

`python3 manage.py makemigrations`  
`python3 manage.py migrate`  
`python3 manage.py runserver`

*On Windows:*   
`celery -A sesc_mate worker --pool=solo`    
`celery -A sesc_mate beat`  

*On Linux:*   
`celery -A sesc_mate worker -B`
