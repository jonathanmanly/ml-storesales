import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



df=pd.read_csv("training_data_processed.csv")
print df.shape
df=df[df['Open']==1]
print df.shape
df=df[df['date_dt']>= '2013-02-01']  #Cut out the first 30 days where the time series are incomplete
print df.shape


df['Customer_momentum']=df['Customer_momentum'].replace((-np.inf,np.inf), 1.)
df['Customer_momentum'] = df['Customer_momentum'].fillna(1)
df['Sales_momentum']=df['Sales_momentum'].replace(np.inf, 1.)
df['Sales_momentum'] = df['Sales_momentum'].fillna(1)
df['InvCompDist']=df['InvCompDist'].replace(np.inf, 1.)
df['InvCompDist'] = df['InvCompDist'].fillna(1)
df['lnCompDist'] = df['lnCompDist'].fillna(1)
df['AvgSalePerCust'] = df['AvgSalePerCust'].fillna(0)
df['EffectiveCompetitionDistance'] = df['EffectiveCompetitionDistance'].fillna(0)


df_train = df[df['date_dt']<= '2015-02-01']
df_test = df[df['date_dt']> '2015-02-01']


trainVars = [x for x in df_train.columns if x not in ['m','date_dt','Sales','Store','Unnamed: 0','StateHoliday']]

trainVars = [x for x in trainVars if 'Store' not in x]


xgb_params = {
    'eta': .01,
    'min_child_weight':1,
    'max_depth': 7,
    'subsample': 0.9,
    'colsample_bytree': 0.9,
    'objective': 'reg:linear',
    'reg_alpha':0.0,
    'reg_lambda':0.0,
    'silent': 1
}

X_train = df_train[trainVars]
X_test = df_test[trainVars]

chk = np.isfinite(X_train).sum()
print chk[chk<len(X_train)]

y_train = np.ravel(df_train['Sales'])
y_test = np.ravel(df_test['Sales'])

dtrain = xgb.DMatrix(X_train, y_train)


cv_output = xgb.cv(xgb_params, dtrain, num_boost_round=2500, early_stopping_rounds=20,verbose_eval=50,show_stdv=False)




xgmodel_full = xgb.train( xgb_params, dtrain, num_boost_round=2000)#,verbose_eval=50, obj = None


y_pred_score  = xgmodel_full.predict(xgb.DMatrix(X_test))

print "R2 is ",r2_score(y_test,y_pred_score)
print "error is ",mean_squared_error(y_test,y_pred_score),mean_squared_error(y_test,y_pred_score)**.5




for thisStore in (817,307,241):
    fig, ax = plt.subplots()
    idx = df_test['Store']==thisStore
    date_labels = df_test['date_dt'][idx]
    x= [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in date_labels]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.plot(x,np.ravel(y_pred_score[idx]),marker='o',label="Predicted",color='red')
    plt.plot(x,np.ravel(y_test[idx]),marker='o',label="Actual",color='blue')
    plt.title("Store number "+str(thisStore)+" - prediction vs actual")
    plt.ylabel("Sales")
    plt.xlabel("Date")
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    legend = ax.legend(loc='lower right', shadow=True)
    plt.gcf().autofmt_xdate()
    plt.savefig("pred_compare"+str(thisStore)+".png")
    plt.clf()





