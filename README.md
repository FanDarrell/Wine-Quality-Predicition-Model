# cs-643-proj2
This is my repository for all code related to CS 643's second programming assignment.

# Step 1: Initialize your EMR Cluster

Begin by navigating to your AWS Academy/Vocareum account, then navigate to Modules > Learner Lab, and click 'Start Lab'

Navigate to EMR, and select create cluster.

Select Spark/Hadoop

Configure your cluster to have 1 primary node and 3 core nodes. You can remove the task nodes group.

Choose a regional subnet that matches your available AWS credentials.

Launch your instance.

From there, navigate to your EC2 instances menu and select your primary node.

Navigate to the security tab, and click on the link underneath security groups.

Add an inbound rule allowing SSH traffic from anywhere

# Step 2: Connect and initialize needed software

SSH into your EMR primary node.

Navigate to teh crednetials file in .aws directory, update it with the keys for your AWS session.

Copy both TrainingDataset.csv and ValidationDataset.csv onto your primary node.

Copy both training.py and predict.py onto your primary node.

Run the following commands:

$ sudo yum update -y
$ pip install flintrock
$ pip install py4j
$ pip install findspark
$ wget http://archive.apache.org/dist/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz
$ sudo tar -zxvf spark-3.0.0-bin-hadoop2.7.tgz 
$ pip install scikit-learn
$ pip install pandas

Commit the training datasets to HDFS:

$ hadoop fs -put TrainingDataset.csv
$ hadoop fs -put ValidationDataset.csv

You can check to see if you've done this successfully by running:

$ hadoop fs -ls

Run training.py to generate the training model using the folloiwng command (note- when entering the address for the files in the following command, use the hdfs locations which should look something like this 'hdfs://ip-172-31-28-22.ec2.internal:8020/user/hadoop/TrainingDataset.csv'):

$ spark-submit --packages org.apache.hadoop:hadoop-aws:2.7.7 /home/hadoop/training.py <location of training set> <location of validation set> <location of training model>

Then, to pull the newly created training model into your local machine, run:

$ hadoop fs -copyToLocal <address of training model>

# Step 3: Creating Docker Image

Ensure you have docker installed by running docker --version and if not run pip install docker

create a director for Docker operations:

$ mkdir dockerImg

Create a Dockerfile of your own or upload mine from this repo:

$ cd dockerImg
$ touch Dockerfile

The contets should look as follows:

FROM centos:7

RUN yum -y update && yum -y install python3 python3-dev python3-pip python3-virtualenv \
	java-1.8.0-openjdk wget

RUN python -V
RUN python3 -V

ENV PYSPARK_DRIVER_PYTHON python3
ENV PYSPARK_PYTHON python3

RUN pip3 install --upgrade pip
RUN pip3 install numpy panda
RUN pip3 install pandas

RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz


RUN ln -s /opt/spark-3.1.2-bin-hadoop2.7 /opt/spark
RUN (echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc && echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc && echo 'export PYSPARK_PYTHON=python3' >> ~/.bashrc)


COPY . /dockerImg


RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN /bin/bash -c "source ~/.bashrc"
RUN /bin/sh -c "source ~/.bashrc"
WORKDIR /dockerImg
ENTRYPOINT ["/opt/spark/bin/spark-submit", "--packages", "org.apache.hadoop:hadoop-aws:2.7.7", "predict.py"]

Additionally, move the training model, validation dataset, and predict.py into the dockerImg directory.

Next, run the following commands:

$ sudo service docker start
$ sudo docker login
$ sudo docker build -t <desired image name> .
$ sudo docker push <image name> <user name>/<repository>:'tag'

# Step 4, initializing an EC2 instance and downloading and running a docker container on it

On your AWS services homepage, navigate to the EC2 section

Launch an instance, select AWS Linux, and SSH into your node.

Run the folowing commands:

$ sudo yum update -y
$ sudo yum install python
$ curl -O https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py --user
$ sudo yum install docker -y
$ sudo service docker start
$ sudo docker login
$ sudo docker pull <username>/<repo>:<tag>
$ sudo docker run <username>/<repo>:<tag>

The program should now be running on the local EC2 instance

# Step 5: Running the application without docker 

Similarly to the last step, launch a single EC2 instance and SSH into it, then run these commands:

Copy the trained ML model, desired data set, and 

$ sudo yum update -y
$ sudo yum install python
$ sudo yum install java
$ curl -O https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py --user
$ pip install py4j
$ pip install findspark
$ pip install scikit-learn
$ pip install pandas
$ python predict.py <model location> <dataset location>

You should now be running the app on your local device








