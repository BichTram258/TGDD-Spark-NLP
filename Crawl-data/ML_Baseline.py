import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.metrics import accuracy_score, classification_report, f1_score
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from keras.layers import Dense, Input, LSTM, Bidirectional, Conv1D
from keras.layers import Dropout, Embedding
from keras.preprocessing import text, sequence
from keras.layers import GlobalMaxPooling1D, GlobalAveragePooling1D, concatenate, SpatialDropout1D
from keras.models import Model
from keras import backend as K
from keras.models import model_from_json
from keras.models import load_model
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from keras_preprocessing.sequence import pad_sequences
import keras
from keras import optimizers
from keras import backend as K
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers import Embedding, Conv1D, MaxPooling1D, GlobalMaxPooling1D
from keras.utils import plot_model
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import os, re, csv, math, codecs


train = pd.read_csv(r'E:\TGDD-Spark-NLP\UIT_ViSFD\Train.csv')
dev = pd.read_csv(r'E:\TGDD-Spark-NLP\UIT_ViSFD\Dev.csv')
test = pd.read_csv(r'E:\TGDD-Spark-NLP\UIT_ViSFD\Test.csv')

aa=['SCREEN','CAMERA','FEATURES','BATTERY','PERFORMANCE','STORAGE','DESIGN','PRICE','GENERAL','SER&ACC']
a =['SCREEN','CAMERA','FEATURES','BATTERY','PERFORMANCE','STORAGE','DESIGN','PRICE','GENERAL','SER&ACC','OTHERS']
s=['Positive','Negative','Neutral']
label=[]
aspect=[]
for i in range(0,10):
    x=[]
    for j in range(0,3):
        x.append(aa[i]+'#'+s[j])
    aspect.append(x)
for i in range (0,10):
    for j in range(0,3):
        label.append(aa[i]+'#'+s[j])
slabel=label.copy()
saspect=aspect.copy()
label.append('OTHERS')
aspect.append(['OTHERS'])

def ag_matrix(df_name,r1,r2,c1=5,c2=37,l=label):
    df=df_name.copy()
    for i in range(0,len(l)):
        df[l[i]]=0
    for i in range(r1,r2):
        for j in range(0,len(l)):
            if l[j] in str(df['label'][i]):
                df[l[j]][i]=1
    m=df.iloc[r1:r2,c1:c2]
    return m

def aspect_matrix(df_name,r1,r2):
    if r1==0:
      kk=pd.DataFrame(np.zeros((11,r2-r1))).T
      kk.columns=a
    else:
      kk=pd.DataFrame(np.zeros((11,r2-r1+1))).T
      kk.columns=a
    w=0
    for i in range(r1,r2):
        kk['SCREEN'][w]=max(df_name['SCREEN#Positive'][i], df_name['SCREEN#Negative'][i], df_name['SCREEN#Neutral'][i])
        kk['CAMERA'][w]=max(df_name['CAMERA#Positive'][i], df_name['CAMERA#Negative'][i], df_name['CAMERA#Neutral'][i])
        kk['FEATURES'][w]=max(df_name['FEATURES#Positive'][i], df_name['FEATURES#Negative'][i], df_name['FEATURES#Neutral'][i])
        kk['BATTERY'][w]=max(df_name['BATTERY#Positive'][i], df_name['BATTERY#Negative'][i], df_name['BATTERY#Neutral'][i])
        kk['PERFORMANCE'][w]=max(df_name['PERFORMANCE#Positive'][i], df_name['PERFORMANCE#Negative'][i], df_name['PERFORMANCE#Neutral'][i])
        kk['STORAGE'][w]=max(df_name['STORAGE#Positive'][i], df_name['STORAGE#Negative'][i], df_name['STORAGE#Neutral'][i])
        kk['DESIGN'][w]=max(df_name['DESIGN#Positive'][i], df_name['DESIGN#Negative'][i], df_name['DESIGN#Neutral'][i])
        kk['PRICE'][w]=max(df_name['PRICE#Positive'][i], df_name['PRICE#Negative'][i], df_name['PRICE#Neutral'][i])
        kk['GENERAL'][w]=max(df_name['GENERAL#Positive'][i], df_name['GENERAL#Negative'][i], df_name['GENERAL#Neutral'][i])
        kk['SER&ACC'][w]=max(df_name['SER&ACC#Positive'][i], df_name['SER&ACC#Negative'][i], df_name['SER&ACC#Neutral'][i])
        kk['OTHERS'][w]=df_name['OTHERS'][i]
        w+=1
    return kk

def ss_matrix(df_name,r1,r2,c1=5,c2=36,l=slabel):
    df=df_name.copy()
    for i in range(0,len(l)):
        df[l[i]]=0
    for i in range(r1,r2):
        for j in range(0,len(l)):
            if l[j] in str(df['label'][i]):
                df[l[j]][i]=1
    m=df.iloc[r1:r2,c1:c2]
    return m

def senti_matrix(df_name,r1,r2):
    w=0
    #a=['SCREEN','CAMERA','FEATURE','BATTERY','PERFORMANCE','STORAGE','DESIGN','PRICE','GENERAL','OTHERS']
    if r1==0:
      m=pd.DataFrame(np.zeros((10,r2-r1))).T
      m.columns=aa
    else:
      m=pd.DataFrame(np.zeros((10,r2-r1+1))).T
      m.columns=aa
    for x in range(r1,r2):
        for i in range(0,10):
            for j in range(0,3):
                if df_name[saspect[i][j]][x]==1:
                    m[a[i]][w]=j+1
        w+=1
    return m

dd_train=ag_matrix(train,0,len(train))
ddd_train=aspect_matrix(dd_train,0,len(train))
dd_test=ag_matrix(test,0,len(test))
ddd_test=aspect_matrix(dd_test,0,len(test))

ss_train=ss_matrix(train,0,len(train))
sss_train=senti_matrix(ss_train,0,len(train))
ss_test=ss_matrix(test,0,len(test))
sss_test=senti_matrix(ss_test,0,len(test))

Y_train_aspect = ddd_train.astype('int')
Y_test_aspect = ddd_test.astype('int')
Y_train_polarity = ss_train
Y_test_polarity = ss_test

EMBEDDING_FILE= 'E:\TGDD-Spark-NLP\cc.vi.300.vec'
max_features=2489
maxlen=150
embed_size=300

X_train = train['comment']
y_train = dd_train
X_test = test['comment']
y_test = dd_test

tokenizer = text.Tokenizer(num_words=max_features, lower=True)
tokenizer.fit_on_texts(list(X_train))
word_index = tokenizer.word_index

X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

X_train = pad_sequences(X_train, maxlen=maxlen)
X_test = pad_sequences(X_test, maxlen=maxlen)
print("create vector")

embeddings_index = {}
with open(r'E:\TGDD-Spark-NLP\cc.vi.300.vec', encoding='utf-8') as f:
    for line in f:
        values = line.strip().split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
        
embedding_dim = 300
embedding_matrix = np.zeros((max_features, embedding_dim))

for word, i in word_index.items():
    if i >= max_features:
        continue

    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector[:embedding_dim]

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

#training params
batch_size = 32
epochs =20

#model parameters
num_filters = 64
embed_dim = 300
weight_decay = 1e-4

print("training CNN ...")
model = Sequential()
model.add(Embedding(max_features, embed_size,
          weights=[embedding_matrix], input_length=maxlen, trainable=False))
model.add(Conv1D(num_filters, 7, activation='relu', padding='same'))
model.add(MaxPooling1D(2))
model.add(Conv1D(num_filters, 7, activation='relu', padding='same'))
model.add(GlobalMaxPooling1D())
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Dense(11, activation='sigmoid'))  #multi-label (k-hot encoding)

adam = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
model.summary()

early_stopping = EarlyStopping(monitor='val_loss', min_delta=0.01, patience=4, verbose=1)
callbacks_list = [early_stopping]
y_train = ddd_train
hist = model.load_weights(r'E:\TGDD-Spark-NLP\Crawl-data\cnn_aspect.h5')

y_test = ddd_test
predictions = model.predict(X_test, batch_size=batch_size, verbose=1)

ddd_train
pre=pd.DataFrame(predictions)
aspect = ddd_test.columns.tolist()
pre.columns=aspect
y_test = ddd_test
score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=1)
print('Test accuracy cnn aspest:', score)

# c_pre=pre.copy()
# for i in range(0,c_pre.shape[0]):
#   for j in range(0,len(aspect)):
#     if c_pre[aspect[j]][i]>=0.5:
#       c_pre[aspect[j]][i]=1
#     else:
#       c_pre[aspect[j]][i]=0
      
# print(classification_report(y_test, c_pre, target_names=aspect))

inp = Input(shape=(maxlen,))

x = Embedding(max_features, embed_size, weights=[embedding_matrix], trainable=True)(inp)
x = SpatialDropout1D(0.35)(x)

x = Bidirectional(LSTM(128, return_sequences=True, dropout=0.15, recurrent_dropout=0.15))(x)
x = Conv1D(64, kernel_size=3, padding='valid', kernel_initializer='glorot_uniform')(x)

avg_pool = GlobalAveragePooling1D()(x)
max_pool = GlobalMaxPooling1D()(x)
x = concatenate([avg_pool, max_pool])

out = Dense(11, activation='sigmoid')(x)

model = Model(inp, out)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc',f1_m,precision_m, recall_m])
model.summary()

batch_size = 32
epochs =20

model.load_weights(r'E:\TGDD-Spark-NLP\Crawl-data\lstm.h5')

predictions = model.predict(X_test, batch_size=batch_size, verbose=1)

print(predictions)

pre=pd.DataFrame(predictions)
pre.columns=aspect

score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=1)
print('Test accuracy lstm:', score)