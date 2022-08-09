"""
This visualization will show the chart with the following 
1. Simple Moving Avg (high, close, hlc3)
2. Exponential Moving Avg (high, close, hlc3)
3. ADX, ADXR
"""
from __future__ import annotations
from re import X
from tkinter import Y
from turtle import color, width
from numpy import size
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime

def vizADXCobra(symbols, dfBase, dateWindow, dfSupportLines, dfResistanceLines, MADXCobraParams, executionParams, dfMySymbols=pd.DataFrame()):

    if (len(symbols) == 0): #if there are no symbols that met the conditions, display a message and return
        fig = go.Figure()
        fig.update_layout(
            xaxis = {'visible':False},
            yaxis = {'visible':False},
            annotations = [{
                'text': 'No symbols to display :( ',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size':28}
            }]
        )
        fig.show()
        return

    windowType = dateWindow['windowType'] # resolved window type
    startDate = dateWindow['startDate'] # resolved start date
    endDate = dateWindow['endDate'] # resolved end date    

    adxLowerLimit = MADXCobraParams['adxLowerLimit']
    adxUpperLimit = MADXCobraParams['adxUpperLimit']


    for symbol in symbols: # draw the chart for each symbol in the suggested symbols list
        dfSymbol = dfBase.loc[(dfBase['symbol']==symbol) & (dfBase['SMAhigh']>0)] # get the data for the symbol that is currently in loop

        latestHigh = dfSymbol['High'][dfSymbol.index[-1]] #the most recent high price
        latestLow = dfSymbol['Low'][dfSymbol.index[-1]] #the most recent low price


        candlesticks = go.Candlestick( # draw candlesticks
            x=dfSymbol['Date'],
            open = dfSymbol['Open'],
            close = dfSymbol['Close'],
            high = dfSymbol['High'],
            low = dfSymbol['Low'], 
            name='Candles'
        )

        SMA_hlc3 = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['SMAhlc3'],
            mode='lines',
            name='SMA HLC3',
            line = dict(color='black', width=2)
        )
        SMA_high = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['SMAhigh'],
            mode='lines',
            name='SMA High',
            line = dict(color='black', width=1)
        )
        SMA_low = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['SMAlow'],
            mode='lines',
            name='SMA Low',
            line = dict(color='black', width=1)
        )
        EMA_hlc3 = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['EMAhlc3'],
            mode='lines',
            name='EMA HLC3',
            line = dict(color='blue', width=2)
        )
        EMA_high = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['EMAhigh'],
            mode='lines',
            name='EMA High',
            line = dict(color='blue', width=1)
        )
        EMA_low = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['EMAlow'],
            mode='lines',
            name='EMA Low',
            line = dict(color='blue', width=1)
        )
        ADX = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['ADX'],
            mode='lines',
            name='ADX',
            line = dict(color='green', width=1)
        )        
        ADXR = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['ADXR'],
            mode='lines',
            name='ADXR',
            line = dict(color='blue', width=1)
        )            

        # Create subplots and mention plot grid size
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.03,  
               row_width=[0.2, 0.7])
        #fig = go.Figure()     
        fig.add_trace(candlesticks)
        fig.add_trace(SMA_hlc3)
        fig.add_trace(SMA_high)
        fig.add_trace(SMA_low)
        fig.add_trace(EMA_hlc3)
        fig.add_trace(EMA_high)
        fig.add_trace(EMA_low)

        fig.add_trace(ADX, row=2, col=1)
        #fig.add_trace(ADXR, row=2, col=1)

        fig.update_layout( # to update the chart title with date window information
            title=go.layout.Title(
                text = symbol + "<br><sup>" + windowType + ": " + startDate.strftime("%Y/%m/%d") + " to " + endDate.strftime("%Y/%m/%d") + "</sup>",
                xref = "paper", 
                x=0)
            )
        fig.add_hline(y=adxLowerLimit, line_dash='dot', row=2, col=1, annotation_text='Lower Limit - '+str(adxLowerLimit), annotation_position="bottom right", line_color='grey', line_width=1)
        fig.add_hline(y=adxUpperLimit, line_dash='dot', row=2, col=1, annotation_text='Upper Limit - '+str(adxUpperLimit), annotation_position="bottom right", line_color='grey', line_width=1)

        # add resistance lines
        for index, row in dfResistanceLines.loc[dfResistanceLines['symbol']==symbol].iterrows():
            avgHigh = round(row['avgHigh'],2)
            similarTops = int(row['similarTops'])
            annotation_text = str(avgHigh) + ' with ' + str(similarTops) + ' times between ' + str(startDate) + ' and ' + str(endDate) + ' (' + str(row['rankTops']) + ')'
            if avgHigh <= (latestHigh* (1+MADXCobraParams['resistnaceLimitPct']/100)): # ignore the lines that are 25% above the latest high
                fig.add_hline(y=avgHigh, row=1, col=1, annotation_text=annotation_text, annotation_position='top left', line_color='orange', line_width=1)
            
        for index, row in dfSupportLines.loc[dfSupportLines['symbol']==symbol].iterrows():
            avgLow = round(row['avgLow'],2)
            similarBottoms = row['similarBottoms']
            annotation_text = str(avgLow) + ' with ' + str(similarBottoms) + ' times between ' + str(startDate) + ' and ' + str(endDate) + ' (' + str(row['rankBottoms']) + ')'
            if avgLow >= (latestLow*(1-MADXCobraParams['supportLimitPct']/100)):
                fig.add_hline(y=avgLow, row=1, col=1, annotation_text= annotation_text, annotation_position='top left', line_color='darkturquoise', line_width=1)

        fig.update(layout_xaxis_rangeslider_visible=False) # to turn off the range slider at the bottom of the chart


        if executionParams['type'] == 'track': # for my symbols to track them
            purchasedDate = dfMySymbols.loc[dfMySymbols['symbol']==symbol, 'purchasedDate'].values[0]
            purchasedDate = datetime.datetime.strptime(purchasedDate, "%m/%d/%Y").timestamp() * 1000
            purchasedPrice = dfMySymbols.loc[dfMySymbols['symbol']==symbol, 'purchasedPrice'].astype(float).values[0]
            fig.add_trace(go.Scatter(x=[purchasedDate], y=[purchasedPrice],name='Purchase', mode='markers', marker=dict(color='LightSkyBlue', size=20),showlegend=True))

            fig.update_layout(
                #paper_bgcolor='rgba(161,232,231,1)', #blue'ish
                #plot_bgcolor='rgba(250,114,60,0.33)' #purple'ish
                paper_bgcolor='rgba(200,200,200,0.2)',
                plot_bgcolor='rgba(200,200,200,0.2)'
            )



        fig.show() # display the chart    


