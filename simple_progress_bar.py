
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


# In[31]:

from IPython.core.display import display
import urllib, json
from ipywidgets import FloatProgress,HTML,HBox
from IPython.lib import backgroundjobs

#Create progress bar
def create_html():
    data = [0]
    jobs = {}
    #initialize float progress bar widget
    f = FloatProgress(min=0, max=100)
    #initialize html widget
    l = HTML()
    #initialize horizontal box with 2 elements
    box = HBox(children=[f, l])
    display(box)
    
    while not jobs:
        while len(data)>0:
            #get details of running jobs
            url = "http://localhost:4040/api/v1/applications/"+ str(sc.applicationId) +"/jobs?status=running"
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            for i in data:
                #storing task details for each jobs separately
                jobs[i['jobId']] = {
                    'active_task': i["numActiveTasks"],
                    'completed_task': i["numCompletedTasks"],
                    'failed_task': i["numFailedTasks"],
                    'total_task': i["numTasks"]
                }
                #updating content of html
                l.value = "{} Tasks Completed".format(str(jobs[i['jobId']]['completed_task']),str(jobs[i['jobId']]['total_task']))
                value = float(jobs[i['jobId']]['completed_task'])*100.0/float(jobs[i['jobId']]['total_task'])
                #updating value of progress bar
                f.value = value
                #print jobs
        #get all completed jobs
        url = "http://localhost:4040/api/v1/applications/"+ str(sc.applicationId) +"/jobs?status=succeeded"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for i in data:
            #Store completion details of only jobs which was running
            if i['jobId'] in jobs:
                jobs[i['jobId']] = {
                    'active_task': i["numActiveTasks"],
                    'completed_task': i["numCompletedTasks"],
                    'failed_task': i["numFailedTasks"],
                    'total_task': i["numTasks"]
                }
                l.value = "{} Tasks Completed".format(str(jobs[i['jobId']]['completed_task']))
                f.bar_style= 'success'
                f.value = float(jobs[i['jobId']]['completed_task'])*100.0/float(jobs[i['jobId']]['total_task'])
    return
    


# In[32]:

def cal(l):
    def call():
        ss = sc.parallelize(l,4)
        print "Sum {}".format(ss.reduce(lambda x,y: x+y))
    #Using ipython module to run tasks in threads
    jobs = backgroundjobs.BackgroundJobManager()
    #Starting calculation task
    jobs.new(call)
    #Starting monitoring task
    jobs.new(create_html)
    return 


# In[33]:

cal(range(1,20000000))


# In[ ]:


