# A progress monitor for pyspark job 

#### Requirements
* python v2.7.12
* pyspark
* spark v2.1.0
* jupyter 4.3.0

#### Setup
1. Install jupyter
    ```sh
    pip install jupyter
2. Download a version of spark with a package type of pre-built for hadoop 2.7 or later. [Download](http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.7.tgz)
3. Unzip folder
   ```sh
   tar -xvf spark-2.1.0-bin-hadoop2.7.tgz
4. Move the unzipped folder to **/usr/lib** folder
5. Set environment variables Spark Home and update python path
   ```bash
   nano ~/.bashrc
   export SPARK_HOME=/usr/lib/spark
   export PATH=$SPARK_HOME/bin:$PATH
   export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
   export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
6. Install pyspark 
    ```sh
    pip install pyspark
#### Procedure
1. Start jupyter notebook
    ```sh
    jupyter notebook
2. This will open a jupyter dashboard.
3. Upload **simple_progress_bar.ipynb** file using the Upload button on the top right corner of the dashboard.
4. Run each cell using **Shift + Enter**.
5. To see the progress bar working, you can increase the range value in the code on In[33] cell.


