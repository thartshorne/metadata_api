
# coding: utf-8

import pandas as pd
import numpy as np

#Read in the metadata file saved locally (add download from web later)
df = pd.read_csv("FFMetadata20180221.csv", encoding = "cp1252")

list(df.columns.values)

#Create list of possible types
types = ["bin", "cont", "oc", "uc", "string", "ID Number"]
#Create list of possible topics
topics = ["attitudes/expectations/happiness", "behavior", "cognitive skills", "childcare - calendar", "childcare services and availability",
         "childcare center composition", "childcare staff characteristics", "accidents and injuries", "disabilities", "fertility history",
          "health behavior", "health care access and insurance", "height and weight", "medication","mental health", "physical health",
          "sexual health and behavior", "substance use and abuse","child living arrangements", "current partner living arrangements", 'home environment',
          "household composition", "housing status", "parents' living arrangements","residential mobility", "grandparents", "parents' family background",
          "social support","community participation", "neighborhood conditions","age","citizenship and nativity", "language","mortality",
         "race/ethnicity","religion","sex/gender","child support","earnings","expenses","financial assets","household income/poverty",
          "income tax", "material hardship", "private transfers","public transfers and social services","educational attainment/achievement", 
          "parent school involvement", "peer characteristics","school characteristics","school composition",
         "student experiences", "teacher characteristics", "employment - calendar", "employment - traditional work", "employment - non-traditional work",
         "unemployment","work stress/flexibility","criminal justice involvement", "legal custody", "paternity","police contact and attitudes",
         "new partner relationship quality", "new partner relationship status", "parental relationship history","parental relationship quality", 
         "parental relationship status", "paradata","survey weights","child welfare services", "parent-child contact", "parenting abilities", "parenting behavior"] 
#Create list of possible respondents
respondents = ['d','e','f','h','k','m','n','o','p','q','r','s','t','u']
#Create list of sources
sources = ['constructed','idnum','questionnaire','weight']

df['typeTest'] = df.type.isin(types)
print("Following variables failed the type test")
df[df.typeTest==False]['new_name']

df['waveTest'] = df.wave.between(1,6)
print("Following variables have a wave out of range")
df[df.waveTest == False]['new_name']

df['warningTest'] = df.warning.between(0,6) 
print("Following variables have a warning code out of range")
df[df.waveTest == False]['new_name']

df['topic1Test'] = df.topic1.isin(topics)
print("Following variables have a topic1 not in the set of possible topics")
df[df.topic1Test == False]['new_name']

df['scopeTest'] = df.scope.isin([20,16,15,18,2])
print("Following variables have a scope out of range")
df[df.scopeTest == False]['new_name']

df['respondentTest'] = df.respondent.isin(respondents)
print("Following variables failed the respondent test")
df[df.respondentTest == False]['new_name']

df['sourceTest'] = df.source.isin(sources)
print("Following variables failed the source test")
df[df.sourceTest == False]['new_name'] 

#Testing for logical warning code - type combinations
for i, row in df.iterrows():
    #Warning 2 only for continuous variables
    if df.warning.loc[i] == 2:
        if df.type.loc[i] == "cont":
            pass
        else:
            print(df.new_name.loc[i] + " failed warning 2 test -- not continuous")
            print("Type = " + df.type.loc[i])
    #Warning 6 only for binary variables
    if df.warning.loc[i] == 6:
        if df.type.loc[i] == "bin":
            pass
        else:
            print(df.new_name.loc[i] + " failed warning 6 test -- not binary")
            if pd.isnull(df.type.loc[i]) == False:
                print("Type = "+ df.type.loc[i]) 
            else:
                print("Type is missing")

df.drop(['typeTest','warningTest','topic1Test','waveTest', 'sourceTest', 'respondentTest','scopeTest'], axis=1, inplace = True)

