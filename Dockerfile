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
