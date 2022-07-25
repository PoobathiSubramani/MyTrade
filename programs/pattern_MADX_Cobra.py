"""
This program sets up data for applying the MADX Cobra strategy
set up:
    a. Simple Moving Avg
        - SMA<200> for High
        - SMA<200> for (high + Low + close)/3
        - SMA<200> for Low
    b.  Exponential Moving Avg
        - EMA<10> for High
        - EMA<10> for (high + Low + close)/3
        - EMA<10> for Low
    c. ADX (used to detect the strength fo the trend NOT the direction)

Reading the chart:
Long-Term trade (buy at lower price and sell at higher): EMA band is above SMA band
Short-Term trade: EMA band is below SMA band


"""

import talib as ta
import pandas as pd

def MADXCobra(df, params):

    adxLowerLimit = params['adxLowerLimit']
    adxUpperLimit = params['adxUpperLimit']    
    
    dfFinal = pd.DataFrame() # empty dataframe for combining all the symbols one by one thru iteration
    for symbol in df['symbol'].unique(): # iterator for symbols
        dfSymbol = df.loc[df['symbol']==symbol] # create dataset for the current symbol
        maxIndex = dfSymbol.index.max() # get the latest row in the current symbol dataset
        latestLow = dfSymbol.loc[maxIndex, 'Low']
        latestHigh = dfSymbol.loc[maxIndex, 'High']

        # get the values as per the MADX Cobra strategy
        emaLow = ta.EMA(dfSymbol['Low'], timeperiod=params['emaTimePeriod'])
        emaHigh = ta.EMA(dfSymbol['High'], timeperiod=params['emaTimePeriod'])
        emaHLC3 = ta.EMA((dfSymbol['High']+dfSymbol['Low']+dfSymbol['Close'])/3, timeperiod=params['emaTimePeriod'])
        smaLow = ta.SMA(dfSymbol['Low'], timeperiod=params['smaTimePeriod'])
        smaHigh = ta.SMA(dfSymbol['High'], timeperiod=params['smaTimePeriod'])
        smaHLC3 = ta.SMA((dfSymbol['High']+dfSymbol['Low']+dfSymbol['Close'])/3, timeperiod=params['smaTimePeriod'])          
        adx = ta.ADX(dfSymbol['High'],dfSymbol['Low'],dfSymbol['Close'], timeperiod=params['adxTimePeriod'])
        adxr = ta.ADXR(dfSymbol['High'],dfSymbol['Low'],dfSymbol['Close'], timeperiod=params['adxTimePeriod'])        

        # add the values as columns in the dataframe
        dfSymbol['EMAlow']=emaLow
        dfSymbol['EMAhigh']=emaHigh
        dfSymbol['EMAhlc3']=emaHLC3
        dfSymbol['SMAlow']=smaLow
        dfSymbol['SMAhigh']=smaHigh
        dfSymbol['SMAhlc3']=smaHLC3    
        dfSymbol['ADX']=adx
        dfSymbol['ADXR']=adxr
        
        # conditions for action
        dfSymbol.loc[maxIndex, 'action'] = 'buy' if (latestLow > dfSymbol.loc[maxIndex, 'EMAhigh']  # above the SMA High
            and latestLow > dfSymbol.loc[maxIndex, 'SMAhigh'] # above the EMA High
            and dfSymbol.loc[maxIndex, 'ADX'] > adxLowerLimit and dfSymbol.loc[maxIndex, 'ADX'] < adxUpperLimit # ADX is within the lower and upper limits
            ) else None 

        dfFinal = pd.concat([dfFinal, dfSymbol], axis=0)
    return dfFinal


