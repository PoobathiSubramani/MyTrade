"""
this program gets the support and resistance lines for a given node-based dataset
"""

from numpy import int64
import pandas as pd

def getSRLines(df):
    dfSupportLines = pd.DataFrame()
    dfResistanceLines = pd.DataFrame()
    for symbol in df['symbol'].unique():
        # calculate the score for Resistance Lines
        dfSymbolTop = df.loc[df['symbol']==symbol] 
        dfTopSummary = dfSymbolTop.groupby(by=['symbol','startDate','endDate','age','similarTops'])[['avgHigh', 'scoreTops']].mean().reset_index()
        dfTopSummary['similarTops'] = dfTopSummary['similarTops'].astype(int64) #convert to int
        dfTopSummary['rankTops'] = dfTopSummary['scoreTops'].rank(ascending=False).astype(int64)
        currMaxPrice = dfSymbolTop.loc[dfSymbolTop.index.max(), 'High']
        dfTopSummary['currMaxPrice'] = currMaxPrice # get the max price of latest candle 
        dfTopSummary['pctHigher'] =(dfTopSummary['avgHigh'] - currMaxPrice) / currMaxPrice # calculate the pct diff between the latest max price and avg price of the resistance line
        dfTopSummary = dfTopSummary.loc[dfTopSummary['pctHigher']>0] # consider only the +ve values
        dfTopSummary.sort_values(by=['rankTops'], inplace=True)
        dfResistanceLines = pd.concat([dfResistanceLines, dfTopSummary], axis=0)

        #calculate the score for support lines
        dfSymbolBottom = df.loc[df['symbol']==symbol] 
        dfBottomSummary = dfSymbolBottom.groupby(by=['symbol','startDate','endDate','age','similarBottoms'])[['avgLow', 'scoreBottoms']].mean().reset_index()
        dfBottomSummary['similarBottoms'] = dfBottomSummary['similarBottoms'].astype(int64) #convert to int
        dfBottomSummary['rankBottoms'] = dfBottomSummary['scoreBottoms'].rank(ascending=False).astype(int64)
        currMinPrice = dfSymbolBottom.loc[dfSymbolBottom.index.max(), 'Low']
        dfBottomSummary['currMinPrice'] = currMinPrice # get the min price of latest candle 
        dfBottomSummary['pctLower'] =(currMinPrice - dfBottomSummary['avgLow']) / currMinPrice # calculate the pct diff between the latest max price and avg price of the resistance line
        dfBottomSummary = dfBottomSummary.loc[dfBottomSummary['pctLower']>0] # consider only the +ve values
        dfBottomSummary.sort_values(by=['rankBottoms'], inplace=True)
        dfSupportLines = pd.concat([dfSupportLines, dfBottomSummary], axis=0)

    return dfSupportLines, dfResistanceLines