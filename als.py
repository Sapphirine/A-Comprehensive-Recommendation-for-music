
# coding: utf-8

# # ALS Recommendation
# ### Data import

# In[1]:


# tell jupyter where pyspark is
import findspark
findspark.init()


# In[17]:


from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.regression import LinearRegression
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.ml.feature import IndexToString, StringIndexer
import pandas as pd


# In[3]:


df_r = pd.read_csv('./rating.csv',index_col=None)


# In[4]:


df_ = pd.read_csv('./rating_recommendation.csv',index_col=False)


# In[5]:


df_.head()


# ### Feature selection

# In[6]:


SparkConf().setMaster("master").setAppName("ALSExample")
spark = SparkSession.builder.config(conf=SparkConf())


# In[7]:


# Load data as RDD, then transform it to DataFrame format
lines = spark.read.text("./rating_recommendation.csv").rdd
parts = lines.map(lambda row: row.value.split(","))
ratingsRDD = parts.map(lambda p: Row(userId=str(p[0]), songID=str(p[1]),
                                     play_count=int(p[2])))


# In[8]:


rating = spark.createDataFrame(ratingsRDD)


# In[9]:


indexer = StringIndexer(inputCol="userId",outputCol = "userId_digtal")
indexed = indexer.fit(rating).transform(rating)
indexed.show(5)


# In[10]:


indexed.show(3)


# In[11]:


feature = StringIndexer(inputCol="songID",outputCol="songId_digtal")
indexed2 = feature.fit(rating).transform(indexed)
indexed2.show(5)


# In[12]:


(training, test) = indexed2.randomSplit([0.8, 0.2])


# In[13]:


# Build the recommendation model using ALS on the training data

als = ALS(maxIter=10, regParam=0.3, userCol="userId_digtal", itemCol="songId_digtal", ratingCol="play_count",
          coldStartStrategy="drop")
model = als.fit(training)


# In[14]:


# Make predictions and output a RMSE to check the precision
predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="play_count",
                                predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root-mean-square error = " + str(rmse))


# In[15]:


userRecs = model.recommendForAllUsers(10)
userRecs.show(5)


# In[16]:


# Recommend 5 users for top 6 songs
users = indexed2.select(als.getUserCol()).distinct().limit(6)
userSubsetRecs = model.recommendForUserSubset(users, 6)


# ## Deal with Output

# In[18]:


matrix = [[row[0]]+row[1] for row in song_]
result = []
for row in matrix:
    tmp = [row[0]]
    for j in row[1:]:
        tmp.append(j[0])
    result.append(tmp)


# In[19]:


sc =SparkContext(conf=spark)
row = Row('user_ID','song_ID1','song_ID2','song_ID3','song_ID4','song_ID5','song_ID6')
df_output = SparkContext.parallelize([row(result[0][i],result[1][i],result[2][i],result[3][i],                                            result[4][i],result[5][i]) for i in range(5)]).toDF() 


# In[20]:


## get their original id
converter = IndexToString(inputCol="user_ID", outputCol="user_id")
converted = converter.transform(df_test)
for x in range(6):
    converter = IndexToString(inputCol="song_ID"+str(x+1), outputCol="song_id"+str(x+1))
    converted = converter.transform(df_test)   


# In[21]:


final_result=converted[['user_id']+['song_id'+str(i) for i in range(6)]]
final_result.to_csv('./CF_Recommendation.csv',index=False)


# In[25]:


present = pd.read_csv('./CF_Recommendation.csv',index_col=False)
present.head()

