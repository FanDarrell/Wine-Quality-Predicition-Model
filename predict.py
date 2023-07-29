import sys
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.mllib.tree import RandomForestModel
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors


# Establishing Spark and SQL contexts
conf = (SparkConf().setAppName("Project 2"))
sc = SparkContext("local", conf=conf)
sc.setLogLevel("ERROR")
sqlContext = SQLContext(sc)



print("******Reading from the Dataset*******")

#Allow for 
if len(sys.argv) > 1:
    model = RandomForestModel.load(sc, sys.argv[1] )
    print(model)

    # Reading data sets
    df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true', sep=';').load(sys.argv[2])
else:
    model = RandomForestModel.load(sc, '/dockerImg/trainingmodel.model')
    print(model)

    # Reading datasets
    df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true', sep=';').load('/dockerImg/ValidationDataset.csv')

outputRdd = df.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[:11])))

predictions = model.predict(outputRdd.map(lambda x: x.features))
labelsAndPredictions = outputRdd.map(lambda lp: lp.label).zip(predictions)

metrics = MulticlassMetrics(labelsAndPredictions)



print("\n****Final Statistics*****")
print("Weighted f1 Score = %s" % metrics.weightedFMeasure())
print("Weighted precision = %s" % metrics.weightedPrecision)
print("The End")
