import requests as req
import bs4
import matplotlib.pyplot  as plt
import pandas as pd
import time as t


data=req.get('https://www.mohfw.gov.in/').text
soap=bs4.BeautifulSoup(data,'html.parser')
table=soap.find_all('li')
def seprateing(r):
    table_list=[]
    for i in r:
        table_list.append(i.text.replace('\n',''))
        #print(i.text.replace('\ n',''))
    return table_list
data_set = []
for row in table:
    a= separating(row.find_all('strong',attrs=('class':"mob-hide")))
    if a!=[]:
        data_set.append(a)
l=[]
for l in data_set:
    l.append(int(i[1][:7].replace('\xa0',' ')))
l.append(sum(l))
      
#-------------------------------make a pie chart-------------------------

'''l=[]
for i  in soap.find_all('strong')[6:10]:
    l.append(i.text.replace('\n',''))
print(l)
ldf=pd.DataFrame(l)
print(ldf)'''

temp= 1[:3]
print(l)

temp=l[:3]
print(temp)
plt.pie(x=temp,labels=['Active_Case','Recovery','Death'],wedgeprops={'linewidth':1,'edgecolor':'k'},autopct='%.2f',explode=(0,0,1))
plt.show()

#-------------------------save data in excel file-------------
df=pd.DataFrame([1],columns=['Active Cases', 'Recovered', 'Death', 'Confirmed'])
def data_maintain():
    try:
        data=pd.read_excel('covid19.xlsx')
        if(data.iloc[-1,1]!=str(t.localtime()[0:3])):
            new_data=df
            new_data['Date']=[time.localtime()[0:3]]
            print(new_data)
            data=data.append(new_data,ignore_index=True,sort=False)
            data.to_excel('covid19.xlsx',index=False)
        else:
            print('Todays data already saved please check again')
    except FileNotFoundError:
        df.to_excel('covid19.xlsx',index=False)
        data=pd.read_excel('covid19.xlsx')
        data['Date']=[time.localtime()[0:3]]
        data.to_excel('covid19.xlsx',index=False)
    print('done..')
data_maintain()
              
#----------------------------plot a graph to show the growth rate---------------------------

data=pd.read_excel('covid19.xlsx')
print(data.tail())

def rating():
    try:

        #remain=data.Confirmed-(data.Recoverd+data.Death)
        plt.figure(figsize=(25,10))
        plt.title('Covid-19 Growth Rating')
        plt.plot(data.Date,data.Confirmed,marker='o',color='orange',markeredgecolor='k')
        plt.plot(data.Date,data.Death,marker='o',color='red',markeredgecolor='k')
        plt.plot(data.Date,data.Recoverd,marker='o',color='green',markeredgecolor='k')
        plt.plot(data.Date,data['Active Cases'],marker='o',markeredgecolor='k')
        '''for index,y in enumerate(data['Recoverd']):
            plt.text(index,y,str(y),fontsize=13)
        for index,y in enumerate(data['Confirmed']):
            plt.text(index,y,str(y),fontsize=13)
        for index,y in enumerate(data['Death']):
            plt.text(index,y,str(y),fontsize=13)
        for index,y in enumerate(remain):
        plt.plot(data.Date.tail(8),data.Confirmed.tail(8),marker='o',color='orange',markeredgecolor='k')
        plt.plot(data.Date.tail(8),data.Death.tail(8),marker='o',color='red',markeredgecolor='k')
        plt.plot(data.Date.tail(8),data.Recoverd.tail(8),marker='o',color='green',markeredgecolor='k')
        plt.plot(data.Date.tail(8),data['Active Cases'].tail(8),marker='o',markeredgecolor='k')
        for index,y in enumerate(data['Recoverd'].tail(8)):
            plt.text(index,y,str(y),fontsize=13)
        for index,y in enumerate(data['Confirmed'].tail(8)):
            plt.text(index,y,str(y),fontsize=13)
        for index,y in enumerate(data['Death'].tail(8)):
            plt.text(index,y,str(y),fontsize=13)
        for index,y in enumerate(data['Active Cases'].tail(8)):
            plt.text(index,y,str(y),fontsize=13)
        '''
        plt.show()
    except TypeError:
        print('exception occures')
        data_maintain()
        rating()
rating()
