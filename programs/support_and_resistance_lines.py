"""
this program gets the support and resistance lines for a given node-based dataset
"""

import pandas as pd
import numpy as np


def getSRLines(df):
    dfTopSummary = df.loc[df['isTop']==True].groupby(by=['symbol','startDate','endDate','age','similarTops'])['avgHigh'].mean().reset_index()
    #calculate the score and then the rank of nodes
    #dfTopSummary['scoreTops'] = np.exp(df['age']*(-1)) * np.exp(df['similarTops'])
    print(dfTopSummary)
    dfTopSummary['scoreTops'] = dfTopSummary['age'] * dfTopSummary['similarTops']/0.33
    dfTopSummary['rankTops'] = dfTopSummary['scoreTops'].rank(ascending = True)    
    #dfTopSummary = dfTopSummary.sort_values(by=['symbol','similarTops','avgHigh','startDate','endDate','age'], ascending=[True, False, False, False, False,False])
    dfTopSummary = dfTopSummary.sort_values(by=['symbol','rankTops'], ascending=[True, True])
    print(dfTopSummary)
    dfBottomSummary = df.loc[df['isBottom']==True].groupby(by=['symbol','startDate','endDate','age','similarBottoms'])['avgLow'].mean().reset_index()
    dfBottomSummary['scoreBottoms'] = np.exp(df['age']*(-1)) * np.exp(df['similarBottoms'])
    dfBottomSummary['rankBottoms'] = dfBottomSummary['scoreBottoms'].rank(ascending = False)       
    dfBottomSummary = dfBottomSummary.sort_values(by=['symbol','similarBottoms','avgLow','startDate','endDate','age'], ascending=[True, False, False, False, False, False])
    print(dfBottomSummary)
    return dfTopSummary, dfBottomSummary

