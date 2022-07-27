"""
program finds 
1. the nodes that are switching direction from low to high or high to low
2. the count of nodes that are within a specific tolerance percentage value of the given node's low or high value
"""
from numpy import datetime64, int64
import numpy as np
import pandas as pd
import datetime

def findNodes(df, tolerancePct):
    print('update: finding the similar tops and bottoms for all the symbols is starting.')
    today = datetime.date.today()
    dfFinal = pd.DataFrame()
    for symbol in df['symbol'].unique(): #iterate for each symbol
        
        # find top and bottom nodes for the symbol in current iteration
        dfSymbol = pd.DataFrame() #reset the dataframe for the symbol in current iteration
        dfSymbol = df.loc[df['symbol']==symbol] #create a subset of the symbol in the current iteration
        dfSymbol.reset_index(inplace=True, drop=True) # reset index 
        nodeCount = dfSymbol.shape[0] # get the total rows to find the relative position wrt to the current iteration in the loop
        #dfSymbol['reversalLocation'] = None # set value to none

        #for symbolRowNum in dfSymbol['symbolRowNum'].astype(np.int64): # iterate thru all the nodes in the current symbol subset
        for index in dfSymbol.index:
            # when starting the iteration, there will not be a prev node. so, to give advantage to the current node, the following override helps
            prevLow = float('inf') if index == 0 else dfSymbol.loc[index-1, 'Low'] #for the 1st node, set the prev node to hypothetical high
            currLow = dfSymbol.loc[index, 'Low']
            nextLow = float('inf') if index == nodeCount-1 else dfSymbol.loc[index+1, 'Low'] #for the last node, set the next node to hypothetical high

            prevHigh = float('-inf') if index == 0 else dfSymbol.loc[index-1, 'High'] #for the 1st node, set the next node to hypothetical low
            currHigh = dfSymbol.loc[index, 'High']
            nextHigh = float('-inf') if index == nodeCount-1 else dfSymbol.loc[index+1, 'High'] #for the last node, set the next node to hypothetical low

            dfSymbol.loc[index, 'isBottom'] = True if (currLow < prevLow and currLow < nextLow) else False # current node's low is lower than previoius and next node's low
            dfSymbol.loc[index, 'isTop'] = True if (currHigh > prevHigh and currHigh > nextHigh) else False  # current node's high is higher than prev and next node's high

        # find the similar node count for the top and bottom nodes
        dfSymbolBottoms = dfSymbol.loc[dfSymbol['isBottom']==True] # temp df for only the bottom nodes
        dfSymbolTops = dfSymbol.loc[dfSymbol['isTop']==True] # temp df for only the top nodes
        for index in dfSymbol.index:
            
            fibMax = dfSymbol['High'].max()
            fibMin = dfSymbol['Low'].min()
            fibDiff = fibMax - fibMin
            fib100pct = fibMax
            

            if not (dfSymbol.loc[index, 'isBottom']==True or dfSymbol.loc[index, 'isTop']==True):
                continue # skip the rows that are neither top not bottom

            if (dfSymbol.loc[index, 'isBottom']): #only for the bottom nodes
                bottomLowLimit = dfSymbol.loc[index, 'Low'] * (1-tolerancePct/100)
                bottomHighLimit = dfSymbol.loc[index, 'Low'] * (1+tolerancePct/100)

                # create a temp dataset that meets the criteria. get the summary from that and update that on the row in the current loop.
                dfTempBottom = dfSymbolBottoms.loc[(dfSymbolBottoms['Low']>=bottomLowLimit) & (dfSymbolBottoms['Low']<=bottomHighLimit)]
                #similarBottoms = dfSymbolBottoms.loc[(dfSymbolBottoms['Low']>=bottomLowLimit) & (dfSymbolBottoms['Low']<=bottomHighLimit)].shape[0]
                #dfSymbol.loc[index, 'similarBottoms'] = similarBottoms if similarBottoms > 0 else None

                similarBottoms = dfTempBottom.shape[0] # get the number of rows that meets the tolerance criteria  
                avgLow = dfTempBottom['Low'].mean() # get the avg low price for the criteria
                startDate, endDate = dfTempBottom['Date'].agg(['min','max']) # get the start and end date of the row(s) that meet the criteria                

                if similarBottoms > 0:
                    dfSymbol.loc[index, 'similarBottoms'] = similarBottoms
                    dfSymbol.loc[index, 'avgLow'] = avgLow
                    dfSymbol.loc[index, 'startDate'] = startDate
                    dfSymbol.loc[index, 'endDate'] = endDate
                    dfSymbol.loc[index, 'age'] = (pd.to_datetime(today) - pd.to_datetime(endDate)).days  # find the age of end date from today
                    dfSymbol.loc[index, 'duration'] = (endDate - startDate).days # find the duration of the span
                    dfSymbol.loc[index, 'scoreBottoms'] = (dfSymbol.loc[index, 'similarBottoms']/dfSymbol.loc[index, 'age'])*dfSymbol.loc[index, 'duration'] # my own calc to decide the score
                    #dfSymbol.loc[index, 'rankBottoms'] = dfSymbol['scoreBottoms'].rank(ascending = False)

                similarBottoms = 0 # reset count  
                dfTempBottom.drop(dfTempBottom.index, inplace=True) # drop the dataframe for the next iteration use 

            if (dfSymbol.loc[index, 'isTop']): #  only for the top nodes
                topLowLimit = dfSymbol.loc[index, 'High'] * (1-tolerancePct/100)
                topHighLimit = dfSymbol.loc[index, 'High'] * (1+tolerancePct/100)

                # create a temp dataset that meets the criteria. get the summary from that and update that on the row in the current loop.
                dfTempTop = dfSymbolTops.loc[(dfSymbolTops['High']>=topLowLimit) & (dfSymbolTops['High']<=topHighLimit)]
                print(dfTempTop)
                similarTops = dfTempTop.shape[0] # get the number of rows that meets the tolerance criteria  
                avgHigh = dfTempTop['High'].mean() # get the avg high price for the criteria
                startDate, endDate = dfTempTop['Date'].agg(['min','max']) # get the start and end date of the row(s) that meet the criteria    
                
                if similarTops > 0:
                    dfSymbol.loc[index, 'similarTops'] = similarTops
                    dfSymbol.loc[index, 'avgHigh'] = avgHigh
                    dfSymbol.loc[index, 'startDate'] = startDate
                    dfSymbol.loc[index, 'endDate'] = endDate
                    dfSymbol.loc[index, 'age'] = (pd.to_datetime(today) - pd.to_datetime(endDate)).days # find the age of end date from today
                    dfSymbol.loc[index, 'duration'] = (endDate - startDate).days # find the duration of the span
                    dfSymbol.loc[index, 'scoreTops'] = (dfSymbol.loc[index, 'similarTops']/dfSymbol.loc[index, 'age'])*dfSymbol.loc[index, 'duration'] # my own calc to decide the score
                    #dfSymbol.loc[index, 'rankTops'] = dfSymbol['scoreTops'].rank(ascending = False)

                similarTops = 0 # reset count     
                dfTempTop.drop(dfTempTop.index, inplace=True) # drop the dataframe for the next iteration use     
        
        print('update: finding the similar tops and bottoms for the symbol {} is completed.'.format(symbol))
        dfFinal = pd.concat([dfFinal, dfSymbol], axis=0) # adding the current symbol with the full dataset
    
    
    print('update: finding the similar tops and bottoms for all the symbols is completed.')
    dfFinal = dfFinal.loc[(dfFinal['similarTops']>0) | (dfFinal['similarBottoms']>0) ]

    print('dfFinal types:', dfFinal.dtypes)
    return dfFinal
            

