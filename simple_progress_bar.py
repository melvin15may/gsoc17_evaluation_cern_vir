
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


# In[20]:

from IPython.core.display import display
import urllib, json
from ipywidgets import FloatProgress,HTML,HBox,VBox
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
    stageBox =VBox(children=[])
    display(box)
    
    stage_html = HTML(value="")
    stage_url = "http://localhost:4040/api/v1/applications/"+ str(sc.applicationId) +"/stages/"
    
    #Get more details about the stages in a job and the tasks
    def stage_task(jobId):
        stage_children = []
        for s in i['stageIds']:
            response = urllib.urlopen(stage_url + str(s))
            stage_data = json.loads(response.read())[0]
            value = "<hr><h3> Stage ID: {} <small><strong>{}</strong></small></h3><p>Run time: {} ms</p><p>CPU time: {} ms</p>".format(
                s,
                stage_data["status"],
                stage_data["executorRunTime"],
                stage_data["executorCpuTime"]
            )
            task_box_children = []
            for t in stage_data['tasks']:
                task_box_children.append(
                    HTML(
                        value="<h4>Task ID {} <small>{}</small></h4><p>Deserialize Time: {} ms</p><p>Deserialize CPU Time: {} ms</p><p>Run Time: {} ms</p><p>CPU Time : {} ms</p>".format(
                            t,
                            "COMPLETE" if (stage_data['tasks'][t]['taskMetrics']['executorRunTime'] > 0) else "RUNNING",
                            stage_data['tasks'][t]['taskMetrics']['executorDeserializeTime'],
                            stage_data['tasks'][t]['taskMetrics']['executorDeserializeCpuTime'],
                            stage_data['tasks'][t]['taskMetrics']['executorRunTime'],
                            stage_data['tasks'][t]['taskMetrics']['executorCpuTime']
                        )
                    )
                )
            stage_children+=[HTML(value=value),HBox(children=task_box_children)]
        stageBox.children= stage_children
    display(stageBox)   
    
        
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
                stage_task(i['jobId'])
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
                    'total_task': i["numTasks"],
                    'stages':[]
                }
                l.value = "{} Tasks Completed".format(str(jobs[i['jobId']]['completed_task']))
                f.bar_style= 'success'
                f.value = float(jobs[i['jobId']]['completed_task'])*100.0/float(jobs[i['jobId']]['total_task'])
                
                stage_task(i['jobId'])
        

                
    return
    


# In[4]:

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


# In[5]:

def sync_cal(l):
    ss = sc.parallelize(l,4)
    jobs = backgroundjobs.BackgroundJobManager()
    jobs.new(create_html)
    return ss.reduce(lambda x,y: x+y)


# In[21]:

sync_cal(range(1,20000000))

