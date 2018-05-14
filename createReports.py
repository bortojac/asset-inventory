# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import xml.etree.cElementTree as et
import pandas as pd
import numpy as np
import json

# read in company3 data
company3Pnl = pd.read_csv('reports/company3_pnl.csv',
                      dtype={'self_price': float, 'average_price': float, 'pnl_per': float, 'day_pnl': float },
                      )
company3Pnl.columns = ['day', 'asset', 'selfPrice', 'avgPrice', 'pnlPer', 'pnl']
company3Pnl = (company3Pnl
           .sort_values(['asset', 'day'])
           .assign(asset = lambda x: x.asset.str.lower())
           )

company3Exceptions = pd.read_csv('reports/company3_exception.csv')
 
#def getTransDF():
def readCompany1Xml():
    parsedXml = et.parse("data/raw/Company1.xml")
    transCols = ['company', 'day', 'asset', 'transactions', 'counterparty']
    transDF = pd.DataFrame(columns=transCols)
    priceCols = ['company', 'day', 'asset', 'selfPrice']
    priceDF = pd.DataFrame(columns=priceCols)
    typeToAsset = { '1': 'bonds', '2': 'options', '3': 'stocks' }
    company1StartInvDict = {}
    company = 'Company1'
    for node in parsedXml.getroot():
        if node.tag == 'AssetTransactions':
            for child in node:
                day = child.attrib.get('day')
                asset = typeToAsset[child.attrib.get('type')]
                transactions = child.attrib.get('amount')
                counterparty = child.attrib.get('counterparty')
                series = pd.Series([company, day, asset, transactions, counterparty], index=transCols)
                transDF = transDF.append(series, ignore_index=True)
        if node.tag == 'Prices':
            for child in node:
                day = child.attrib.get('day')
                asset = child.attrib.get('type')+'s'
                selfPrice = child.attrib.get('price')
                series = pd.Series([company, day, asset, selfPrice], index=priceCols)
                priceDF = priceDF.append(series, ignore_index=True)
        if node.tag == 'AssetTypes':
            for child in node:
                asset = child.findtext('Name').lower()
                company1StartInv = child.attrib.get('start_level')
                company1StartInvDict[asset] = int(company1StartInv)
    transDF.to_csv('data/company1/transDF.csv', index=False)
    priceDF.to_csv('data/company1/priceDF.csv', index=False)
    with open('data/company1/company1StartInvDict.json', 'w') as fp:
        json.dump(company1StartInvDict, fp)
    return { 'company1StartInvDict': company1StartInvDict, 'transDF': transDF, 'priceDF': priceDF }
 
            
def calculateCompany1(company1StartInvDict = { 'options': 40, 'bonds': 30, 'stocks': 315 }, transDF = pd.read_csv('data/company1/transDF.csv'), priceDF = pd.read_csv('data/company1/priceDF.csv')): 

    arr = []
    def groupAdd(x):
        grouped = x.groupby('asset')
        for group in grouped.groups:
            arr.append(grouped.get_group(group).transactions.cumsum() + company1StartInvDict[group])
        return pd.concat(arr)            
    
    transDFGrouped = (transDF
                      .assign(transactions = lambda x: pd.to_numeric(x.transactions),
                              day = lambda x: pd.to_numeric(x.day)
                              )
                      .groupby(by=['company', 'day', 'asset'], as_index=False)
                      .agg({'transactions': 'sum'})
                      .sort_values(['asset', 'day'])
                      )
    
    priceDFGrouped = (priceDF
                      .assign(selfPrice = lambda x: pd.to_numeric(x.selfPrice),
                              day = lambda x: pd.to_numeric(x.day)
                              )
                      .groupby(by=['company', 'day', 'asset'], as_index=False)
                      .agg({'selfPrice': 'sum'})
                      .sort_values(['asset', 'day'])
                      )
    
    company1DF = (transDFGrouped
             .merge(priceDFGrouped, how='left', on=['company', 'day', 'asset'])
             .merge(company3Pnl[['day', 'asset', 'avgPrice']], how='left', on=['day', 'asset'])
             .assign(pnlPer = lambda x: x.selfPrice - x.avgPrice,
                     pnl = lambda x: (x.selfPrice - x.avgPrice) * x.transactions,
                     inventory = lambda x: groupAdd(x)                 )
             )
           
    company1DF = (company1DF
              .assign(sod = lambda x: x.inventory - x.transactions,
                      eod = lambda x: x.inventory
                      )
              )
    company1DF = company1DF[['company', 'day', 'asset', 'selfPrice', 'avgPrice', 'pnlPer', 'pnl', 'sod', 'transactions', 'eod']]
    company1PnlDF = company1DF[['day', 'asset', 'selfPrice', 'avgPrice', 'pnlPer', 'pnl']]
    company1Exceptions = company1DF.loc[company1DF.eod < 0, ['day', 'asset', 'sod', 'transactions', 'eod']]
    return { 'company1DF': company1DF, 'company1PnlDF': company1PnlDF, 'company1Exceptions': company1Exceptions }

def writeCompany1Reports():
    returnDict = calculateCompany1()
    company1PnlDF = returnDict['company1PnlDF']
    company1Exceptions = returnDict['company1Exceptions']
    company1PnlDF.to_csv('reports/company1_pnl.csv', index=False)
    company1Exceptions.to_csv('reports/company1_exception.csv', index=False)

readCompany1Xml()
calculateCompany1()
writeCompany1Reports()

def calculateCompany2(company2StartInv = { 'bonds': 380, 'stocks': 140, 'options': 100 }, priceDF = pd.read_excel('data/raw/Company2.XLSX',skiprows=2,usecols=list(range(7,12)),names=['day', 'bonds', 'stocks', 'options']), transDF = pd.read_excel('data/raw/Company2.XLSX',skiprows=8,usecols=list(range(0,4)),names=['day', 'counterparty', 'asset', 'transactions'])):
    
    arr = []
    def groupAdd(x):
        grouped = x.groupby('asset')
        for group in grouped.groups:
            arr.append(grouped.get_group(group).transactions.cumsum() + company2StartInv[group])
        return pd.concat(arr)
    
    company2PriceDF = (priceDF
                   .dropna()
                   .melt(id_vars=['day'],
                         value_vars=['bonds', 'stocks', 'options'],
                         var_name='asset'
                         )
                   .assign(day = lambda x: pd.to_numeric(x.day.str.lower().str.replace("day", "").str.strip()),
                           selfPrice = lambda x: pd.to_numeric(x.value),
                           company = lambda x: pd.Series(np.repeat('company2', x.value.size))
                           )
                   .drop('value', axis=1)
                   .sort_values(['asset', 'day'])
                   .reset_index()
                   .drop('index', axis=1)
                   )
                    
    company2TransDF = (transDF
                   .dropna()
                   .assign(day = lambda x: pd.to_numeric(x.day.str.lower().str.replace("day", "").str.strip())
                    )
                   .reset_index()
                   .drop('index', axis=1)
                   )
    company2TransDF.counterparty = company2TransDF.counterparty.where(company2TransDF.counterparty != 'company3', 'company3')
    company2TransDF.counterparty = company2TransDF.counterparty.where(company2TransDF.counterparty != 'company4', 'company4')
    
    company2TransDFGrouped = (company2TransDF
                          .groupby(['day', 'asset'], as_index=False)
                           .agg({ 'transactions': 'sum' })
                           .sort_values(['asset', 'day'])
                           .reset_index()
                           .drop('index', axis=1)
                           )
    
    company2DF = (company2PriceDF
             .merge(company2TransDFGrouped, how='left', on=['day', 'asset'])
             .merge(company3Pnl[['day', 'asset', 'avgPrice']], how='left', on=['day', 'asset'])
             .assign(pnlPer = lambda x: x.selfPrice - x.avgPrice,
                     pnl = lambda x: (x.selfPrice - x.avgPrice) * x.transactions,
                     inventory = lambda x: groupAdd(x)
                     )
             )
           
    company2DF = (company2DF
              .assign(sod = lambda x: x.inventory - x.transactions,
                      eod = lambda x: x.inventory
                      )
              )
    company2DF = company2DF[['company', 'day', 'asset', 'selfPrice', 'avgPrice', 'pnlPer', 'pnl', 'sod', 'transactions', 'eod']]
    company2PnlDF = company2DF[['day', 'asset', 'selfPrice', 'avgPrice', 'pnlPer', 'pnl']]
    company2Exceptions = company2DF.loc[company2DF.eod < 0, ['day', 'asset', 'sod', 'transactions', 'eod']]
    return { 'company2DF': company2DF, 'company2PnlDF': company2PnlDF, 'company2Exceptions': company2Exceptions }

def writeCompany2Reports():
    returnDict = calculateCompany2()
    company2PnlDF = returnDict['company2PnlDF']
    company2Exceptions = returnDict['company2Exceptions']
    company2PnlDF.to_csv('reports/company2_pnl.csv', index=False)
    company2Exceptions.to_csv('reports/company2_exception.csv', index=False)

calculateCompany2()
writeCompany2Reports()
