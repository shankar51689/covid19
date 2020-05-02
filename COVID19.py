import requests as req
import bs4
import matplotlib.pyplot  as plt
import pandas as pd
import time as t


data=req.get('https://www.mohfw.gov.in/').text
soap=bs4.BeautifulSoup(data,'html.parser')
table=soap.find_all('tr')
def seprateing(r):
    table_list=[]
    for i in r:
        table_list.append(i.text.replace('\n',''))
        #print(i.text.replace('\ n',''))
    return table_list
data_set = []
for row in table:
    data_set.append(seprateing(row.find_all('td')))
data_set=data_set[1:]
del data_set[33:]
for i in range(len(data_set)):
    if(data_set[i][0]!=data_set[len(data_set)-1][0]):
        del data_set[i][0]
    else:
        data_set[i][1]=data_set[i][1].replace('*','')
      
#---------------------make dataframe----------------
    
data_set[17][3]=data_set[17][3].replace('#','')
df=pd.DataFrame(data_set[:len(data_set)],columns=['states','Confirmed','Recoverd','Death'])
print(df)

#-----------------plot the graph----------------------------------------------

df['Confirmed'] = pd.to_numeric(df['Confirmed'])
df['Recoverd'] = pd.to_numeric(df['Recoverd'])
df['Death'] = pd.to_numeric(df['Death'])
df[:len(data_set)-1].plot(kind='bar',x='states',y='Confirmed',color='yellow',figsize=(15,5),edgecolor='k',label='Confirmed')
df[:len(data_set)-1].plot(kind='bar',x='states',y='Recoverd',color='green',figsize=(15,5),edgecolor='k')
df[:len(data_set)-1].plot(kind='bar',x='states',y='Death',color='red',figsize=(15,5),edgecolor='k')
df[:len(data_set)-1].plot.bar(x='states',figsize=(15,5),edgecolor='k')
for index,y in enumerate(df['Confirmed']):
    plt.text(index,y,str(y),fontsize=13)
for index,y in enumerate(df['Recoverd']):
    plt.text(index,y,str(y),fontsize=13)
for index,y in enumerate(df['Death']):
    plt.text(index,y,str(y),fontsize=13)
plt.show()


#-------------------------------make a pie chart-------------------------

l=[]
for i  in soap.find_all('strong')[6:10]:
    l.append(i.text.replace('\n',''))
print(l)
ldf=pd.DataFrame(l)
print(ldf)
plt.pie(x=l,labels=['Remaining','Recovery','Death','Mmigrated'],wedgeprops={'linewidth':1,'edgecolor':'k'},autopct='%.2f',explode=(0,0,0,1))
plt.show()

#-------------------------save data in excel file-------------
try:
    data=pd.read_excel('covid19.xlsx')
    if(data.iloc[-1,-1]!=str(t.localtime()[0:3])):
        new_data=df.iloc[-1:,1:]
        new_data['Date']=[t.localtime()[0:3]]
        data=data.append(new_data,ignore_index=True)
        data.to_excel('covid19.xlsx',index=False)
        print(data)
    else:
        print('Todays data already saved')
except FileNotFoundError:
    df.iloc[33:,0:].to_excel('covid19.xlsx',index=False) 
    data=pd.read_excel('covid19.xlsx')
    data['Date']=[t.localtime()[0:3]]
    data.iloc[:,1:].to_excel('covid19.xlsx',index=False)
print('done..')

#----------------------------plot a graph to show the growth rate---------------------------

remain=data.Confirmed-(data.Recoverd+data.Death)

plt.title('Covid-19 Growth Rating')
plt.plot(data.Date,data.Confirmed,marker='o',color='orange',markeredgecolor='k')
plt.plot(data.Date,data.Death,marker='o',color='red',markeredgecolor='k')
plt.plot(data.Date,data.Recoverd,marker='o',color='green',markeredgecolor='k')
plt.plot(data.Date,remain,marker='o',markeredgecolor='k')

for index,y in enumerate(data['Recoverd']):
    plt.text(index,y,str(y),fontsize=13)
for index,y in enumerate(data['Confirmed']):
    plt.text(index,y,str(y),fontsize=13)
for index,y in enumerate(data['Death']):
    plt.text(index,y,str(y),fontsize=13)
for index,y in enumerate(remain):
    plt.text(index,y,str(y),fontsize=13)
plt.show()