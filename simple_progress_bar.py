
# coding: utf-8

# In[1]:

from pyspark import SparkContext, SparkConf


# In[2]:


#spark conf
conf = ( SparkConf()
         .setMaster("local[*]")
         .setAppName('pyspark')
        )

sc = SparkContext(conf=conf)


# In[16]:

from IPython.core.display import display
import urllib, json
from ipywidgets import FloatProgress,HTML,HBox
from IPython.lib import backgroundjobs
def create_html():
    data = [0]
    jobs = {}
    
    f = FloatProgress(min=0, max=100)
    l = HTML()
    box = HBox(children=[f, l])
    display(box)
    while not jobs:
        while True and len(data)>0:
            url = "http://localhost:4040/api/v1/applications/"+ str(sc.applicationId) +"/jobs?status=running"
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            #print data
            if(len(data) > 0):
                for i in data:
                    jobs[i['jobId']] = {
                        'active_task': i["numActiveTasks"],
                        'completed_task': i["numCompletedTasks"],
                        'failed_task': i["numFailedTasks"],
                        'total_task': i["numTasks"]
                    }
                    l.value = "{} Completed".format(str(jobs[i['jobId']]['completed_task']),str(jobs[i['jobId']]['total_task']))
                    value = float(jobs[i['jobId']]['completed_task'])*100.0/float(jobs[i['jobId']]['total_task'])
                    f.value = value
                #print jobs

        url = "http://localhost:4040/api/v1/applications/"+ str(sc.applicationId) +"/jobs?status=succeeded"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for i in data:
            if i['jobId'] in jobs:
                jobs[i['jobId']] = {
                    'active_task': i["numActiveTasks"],
                    'completed_task': i["numCompletedTasks"],
                    'failed_task': i["numFailedTasks"],
                    'total_task': i["numTasks"]
                }
                l.value = "{} Completed".format(str(jobs[i['jobId']]['completed_task']))
                f.bar_style= 'success'
                f.value = float(jobs[i['jobId']]['completed_task'])*100.0/float(jobs[i['jobId']]['total_task'])
    return
    

# In[17]:

def cal(l):
    def call():
        ss = sc.parallelize(l,4)
        print "Sum {}".format(ss.reduce(lambda x,y: x+y))
    
    jobs = backgroundjobs.BackgroundJobManager()
    jobs.new(create_html)
    jobs.new(call)
    return 


# In[18]:

cal(range(1,20000))


# In[ ]:



