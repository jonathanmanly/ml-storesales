import pandas as pd
import numpy as np
import datetime

start_time = datetime.datetime.now()

print "loading data"
df = pd.read_csv("train.csv",low_memory=False)

allStores = list(set(df['Store']))

store = pd.read_csv("store.csv")



df['date_dt'] = pd.to_datetime(df['Date'])
df['day_of_week'] = df['date_dt'].dt.weekday_name
df['sales_month'] = df['date_dt'].dt.month
df['sales_month'] = df['sales_month'].astype(str)


df['year'] = df['date_dt'].dt.year
#df.drop([u'date_dt'],axis=1,inplace=True)

print "sorting data"

df=df.sort_values(['Store','Date'])



#df=pd.merge(df,store,how='left',left_on='Store',right_on='Store')


store['Promo2_1']=0
store['Promo2_2']=0
store['Promo2_3']=0
store['Promo2_4']=0
store['Promo2_5']=0
store['Promo2_6']=0
store['Promo2_7']=0
store['Promo2_8']=0
store['Promo2_9']=0
store['Promo2_10']=0
store['Promo2_11']=0
store['Promo2_12']=0

print "vectorizing promo2"

for s in range(len(store)):
    if pd.isnull(store.loc[s]['PromoInterval']):
        pass
    elif store.loc[s]['PromoInterval']=='Jan,Apr,Jul,Oct':
        store = store.set_value(s,'Promo2_1',1)
        store = store.set_value(s,'Promo2_4',1)
        store = store.set_value(s,'Promo2_7',1)
        store = store.set_value(s,'Promo2_10',1)
    elif store.loc[s]['PromoInterval']=='Feb,May,Aug,Nov':
        store = store.set_value(s,'Promo2_2',1)
        store = store.set_value(s,'Promo2_5',1)
        store = store.set_value(s,'Promo2_8',1)
        store = store.set_value(s,'Promo2_11',1)
    elif store.loc[s]['PromoInterval']=='Mar,Jun,Sept,Dec':
        store = store.set_value(s,'Promo2_3',1)
        store = store.set_value(s,'Promo2_6',1)
        store = store.set_value(s,'Promo2_9',1)
        store = store.set_value(s,'Promo2_12',1)


store.drop([u'PromoInterval'],axis=1,inplace=True)

print "merging stores and sale days"

df=pd.merge(df,store,how='left',left_on='Store',right_on='Store')


#df['EffectiveCompetitionDistance']=0
#df['NoCompetition']=1
#df['Promo2Effective']=0

print "normalizing promotional and competition data"


df['m']=df['date_dt'].dt.month

df['cf']=1*(df['CompetitionOpenSinceMonth']>=df['date_dt'].dt.month )*(df['CompetitionOpenSinceYear']==df['date_dt'].dt.year)
df['cf2']=1*(df['CompetitionOpenSinceYear']>df['date_dt'].dt.year)
df['competitionActive']=df[['cf','cf2']].max(axis=1)
df['EffectiveCompetitionDistance'] = df['competitionActive']*df['CompetitionDistance']
df=df.drop(['cf','cf2'],axis=1)


df['pr1']=1*(df['Promo2SinceWeek']>=df['date_dt'].dt.week)*(df['Promo2SinceYear']==df['date_dt'].dt.year)
df['pr2']=1*(df['Promo2SinceYear']>df['date_dt'].dt.year)
df['promo2Effective']=df[['pr1','pr2']].max(axis=1)

df['promo2Active'] = (1*df['promo2Effective']*(df['date_dt'].dt.month==1*df['Promo2_1'])+ \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==2*df['Promo2_2']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==3*df['Promo2_3']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==4*df['Promo2_4']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==5*df['Promo2_5']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==6*df['Promo2_6']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==7*df['Promo2_7']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==8*df['Promo2_8']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==9*df['Promo2_9']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==10*df['Promo2_10']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==11*df['Promo2_11']) + \
                    1*df['promo2Effective']*(df['date_dt'].dt.month==12*df['Promo2_12']) )

'''

    if ((df.loc[r]['Promo2SinceWeek']>=df.loc[r]['date_dt'].week and df.loc[r]['Promo2SinceYear']>=df.loc[r]['date_dt'].year)
            or df.loc[r]['Promo2SinceYear']>df.loc[r]['date_dt'].year):
        df['Promo2Effective']=(df.loc[r]['Promo2_1']*(df.loc[r]['date_dt'].month==1)+
            df.loc[r]['Promo2_2']*(df.loc[r]['date_dt'].month==2)+
            df.loc[r]['Promo2_3']*(df.loc[r]['date_dt'].month==3)+
            df.loc[r]['Promo2_4']*(df.loc[r]['date_dt'].month==4)+
            df.loc[r]['Promo2_5']*(df.loc[r]['date_dt'].month==5)+
            df.loc[r]['Promo2_6']*(df.loc[r]['date_dt'].month==6)+
            df.loc[r]['Promo2_7']*(df.loc[r]['date_dt'].month==7)+
            df.loc[r]['Promo2_8']*(df.loc[r]['date_dt'].month==8)+
            df.loc[r]['Promo2_9']*(df.loc[r]['date_dt'].month==9)+
            df.loc[r]['Promo2_10']*(df.loc[r]['date_dt'].month==10)+
            df.loc[r]['Promo2_11']*(df.loc[r]['date_dt'].month==11)+
            df.loc[r]['Promo2_12']*(df.loc[r]['date_dt'].month==12))

'''
print "done normalizing promotional and competition data"

df=df.drop(['CompetitionDistance','Promo2SinceWeek','Promo2SinceYear','CompetitionOpenSinceMonth','CompetitionOpenSinceYear'],axis=1)



#Loop through stores to make lags, then reassemble

df_new = None



for s in allStores:
    print "time shifting",s
    df_store = pd.DataFrame(df[df['Store']==s])
    df_store['Sales30']=df_store['Sales'].shift(30)
    df_store['Sales7']=df_store['Sales'].shift(7)
    df_store['Sales1']=df_store['Sales'].shift(1)
    df_store['Customers30']=df_store['Customers'].shift(30)
    df_store['Customers7']=df_store['Customers'].shift(7)
    df_store['Customers1']=df_store['Customers'].shift(1)
    df_store['StateHoliday1']=df_store['StateHoliday'].shift(1)
    df_store['StateHoliday-1']=df_store['StateHoliday'].shift(-1)
    df_store['SchoolHoliday1']=df_store['SchoolHoliday'].shift(1)
    df_store['SchoolHoliday-1']=df_store['SchoolHoliday'].shift(-1)
    if df_new is None:
        df_new = df_store.copy()
    else:
        df_new = pd.concat([df_new,df_store])

df_new['Sales30'] =df_new['Sales30'].fillna(0)
df_new['Sales7'] =df_new['Sales7'].fillna(0)
df_new['Sales1'] =df_new['Sales1'].fillna(0)
df_new['Customers30'] =df_new['Customers30'].fillna(0)
df_new['Customers7'] =df_new['Customers7'].fillna(0)
df_new['Customers1'] =df_new['Customers1'].fillna(0)
df_new['StateHoliday1'] =df_new['StateHoliday1'].fillna(0)
df_new['StateHoliday-1'] =df_new['StateHoliday-1'].fillna(0)
df_new['SchoolHoliday1'] =df_new['SchoolHoliday1'].fillna(0)
df_new['SchoolHoliday-1'] =df_new['SchoolHoliday-1'].fillna(0)



print "making dummies and merging"
df_new['Store']=df_new['Store'].astype(str)

dummies = pd.get_dummies(df_new[['Store','day_of_week','sales_month','StoreType','Assortment']])
df_new = df_new.drop( ['DayOfWeek', 'Date', 'Customers', 'day_of_week','sales_month', 'year', 'StoreType', 'Assortment', 'Promo2'],axis=1)
df_final = pd.concat([df_new,dummies],axis=1)


print "Final dataset is",df_final.shape

df_final.to_csv("training_data_processed.csv")

print "preprocessing completed in ",datetime.datetime.now()-start_time

