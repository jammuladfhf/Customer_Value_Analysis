
# coding: utf-8

# In[ ]:


#resource for data : https://www.ibm.com/communities/analytics/watson-analytics-blog/marketing-customer-value-analysis/


# In[2]:


import os
os.getcwd()


# In[3]:


import numpy as np            # scintific computing with python
import pandas as pd           # data analysis tool kit    

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt  # for visualization


# In[5]:


df = pd.read_csv('MCVA.csv')


# In[6]:


df.shape


# In[7]:


df.head()


# In[8]:


df.columns


# # Analytics on Engaged customers

# We are going to understand how different customers behaveand react for different marketting  strategies

# ## Over all engagement
# The response field contains information about whether the cusomer responded to the marketing efforts. 

# In[9]:


# get the total noof customer responded for marketing
df.groupby('Response').count()['Customer']


# In[11]:


# visualzing the count
ax = df.groupby('Response').count()['Customer'].plot(
        kind = 'bar',color = 'orchid',grid = True,figsize=(10, 4),title = 'Marketing Engagement')
ax.set_xlabel('Engaged')
ax.set_ylabel('Count')
plt.show()


# In[12]:


# calculating the percentage of engaged and non-engaged customers
df.groupby('Response').count()['Customer']/df.shape[0]


# From the about output we can see that only 14 percent of customers are reponding to the marketing

# # 2.2 Engagement Rates by Offer type  
# The Renewal offer type column in this Data frame contains the type of the renewal  offer presented to the customers.
# we are going to look into what type of  offers worked best for the engaged customers.

# In[13]:


# get the engagement rates per renewal offer
off_type_diff = df.loc[df['Response'] == 'Yes'].groupby(['Renew Offer Type']).count()['Customer']/df.groupby('Renew Offer Type').count()['Customer']


# In[14]:


off_type_diff


# In[15]:


# visualize the bar plot
ax = (off_type_diff*100.0).plot(
    kind = 'bar',
    color = 'green',
    figsize = (10,4),
    grid = True)
ax.set_ylabel('Engagement Rate (%)')
plt.show()


# In[16]:


# Offer type and Vehcle Class
"""We are going to understand how customer with different attributes responding differently to different marketing messages.
we start looking at the engagement rates by  each offer type and vehicle class"""


# In[27]:


by_offer_by_type = df.loc[
                    df['Response'] == 'Yes'].groupby(['Renew Offer Type','Vehicle Class']).count()['Customer'] /df.groupby('Renew Offer Type').count()['Customer']


# In[28]:


by_offer_by_type


# In[29]:


# making the above code more readble by unstacking
by_offer_by_type = by_offer_by_type.unstack().fillna(0)


# In[30]:


by_offer_by_type


# In[33]:


# visualize the data in the bar plot

ax = by_offer_by_type.plot(
        kind = 'bar',
        figsize = (7,7),
        grid = True)
ax.set_ylabel('Engagement rate (%)')
plt.show()


# We already knew from the previous section “Engagement Rates by Offer Type” that Offer2
# had the highest response rate among customers. Now we can add more insights by having broken
# down the customer attributes with the category “Vehicle class”: we can notice that customers with
# Four-Door Car resmpond more frequently for all offer types and that those with “Luxury SUV”
# respond with a higher chance to Offer1 than to Offer2. If we have significantly difference in the
# response rates among different customer rates, we can fine-tune who to target for different set
# of offers

# # Engagemnt Rates by sales channel

# In[45]:


# we are going to see how engagement rates differ by different sales channels.
by_sales_by_channel = df.loc[df['Response'] == 'Yes'].groupby(['Sales Channel']).count()['Customer']/df.groupby('Sales Channel').count()['Customer']


# In[46]:


by_sales_by_channel


# In[54]:


ax = (by_sales_by_channel*100.0).plot(kind = 'bar',grid = True,color = 'palegreen')
ax.set_ylabel('Engagement Rate(%)')


# As we can notice, Agent works better in term of getting responses from the customers, and
# then sales through Web works the second best. Let’s go ahead in breaking down this result deeper
# with different customers’ attributes.

# ###  2.5  -Sales Channel & Vehicle Size

# We are going to see whether customers with various vehicle sizes respond differently to different
# sales channels.

# In[68]:


by_sales_by_channel = df.loc[df['Response'] == 'Yes'].groupby(['Sales Channel','Vehicle Size']).count()['Customer'] / df.groupby('Sales Channel').count()['Customer']


# In[69]:


by_sales_by_channel


# In[70]:


# unstack the above values
by_sales_by_channel = by_sales_by_channel.unstack().fillna(0)


# In[71]:


by_sales_by_channel


# In[75]:


ax = (by_sales_by_channel*100).plot(kind = 'bar',grid = True,figsize = (7,7))
ax.set_ylabel('Engagement (%)')
plt.show()


# ### 2.6 - Engagement Rates by Months Since Policy Inception

# In[87]:


by_mnth_since_pol = df.loc[df['Response'] == 'Yes'].groupby(by='Months Since Policy Inception')['Response'].count() / df.groupby(by = 'Months Since Policy Inception')['Response'].count()*100.0


# In[90]:


by_mnth_since_pol.fillna(0)


# In[96]:


ax = by_mnth_since_pol.fillna(0).plot(grid = True,figsize = (10,7),title = 'Engagement rates by months since inception')
ax.set_ylabel('Engagement(%)')
plt.show()


# ## 3   3. Customer Segmentation by CLV & Months Since Policy Inception
# We are going to segment our customer base by Customer Lifetime Value and Months Since Policy
# Inception.

# In[97]:


# Take a look at distribution 
df['Customer Lifetime Value'].describe()


# For the previous output, we are going to define those customers with a CLV higher than the
# median as high-CLV customers, and those with a CLV lower than the median as low-CLV customers.

# In[98]:


# Customer segmentation
df['Cust_Segm'] = df['Customer Lifetime Value'].apply(lambda x: 'High' if x > df['Customer Lifetime Value'].median() else 'Low')


# In[99]:


# same for Months since Policy inception
df['Months Since Policy Inception'].describe()


# In[100]:


df['Polcy_segm'] = df['Months Since Policy Inception'].apply(lambda x :'High' if x > df['Months Since Policy Inception'].median() else 'Low')


# In[103]:


df.columns


# In[112]:


# visualize this segments
ax = df.loc[(df['Cust_Segm'] == 'High') & (df['Polcy_segm']=='High')
           ].plot.scatter(x = 'Months Since Policy Inception',y = 'Customer Lifetime Value',logy = True,color = 'red')

df.loc[(df['Cust_Segm'] == 'Low') & (df['Polcy_segm']=='High')
      ].plot.scatter(
        ax=ax,
        x = 'Months Since Policy Inception', y = 'Customer Lifetime Value',logy = True,color = 'blue')
df.loc[(df['Cust_Segm'] == 'High') & (df['Polcy_segm'] == 'Low')
      ].plot.scatter(
        ax=ax,
        x = 'Months Since Policy Inception', y = 'Customer Lifetime Value',
        logy = True,
        color = 'orange')
df.loc[(df['Cust_Segm'] == 'Low') & (df['Polcy_segm'] == 'Low')
      ].plot.scatter(
        ax=ax,
        x = 'Months Since Policy Inception', y = 'Customer Lifetime Value',
        logy = True,
        color = 'green',
        grid = True,
        figsize = (10,7))

ax.set_ylabel('CLV(log scale)')
ax.set_xlabel('Months Since plocy Inception')

ax.set_title('Segements by CLV and Policy Age')

plt.show()


