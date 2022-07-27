"""
This visualization will show the chart with the following 
1. Simple Moving Avg (high, close, hlc3)
2. Exponential Moving Avg (high, close, hlc3)
3. ADX, ADXR
"""
from re import X
from tkinter import Y
from turtle import color, width
from unicodedata import name
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def vizADXCobra(dfBase, dateWindow, dfSupportLines, dfResistanceLines, params):
    windowType = dateWindow['windowType'] # resolved window type
    startDate = dateWindow['startDate'] # resolved start date
    endDate = dateWindow['endDate'] # resolved end date    

    adxLowerLimit = params['adxLowerLimit']
    adxUpperLimit = params['adxUpperLimit']

    for symbol in dfBase['symbol'].unique(): # draw the chart for each symbol in the dataset
        dfSymbol = dfBase.loc[(dfBase['symbol']==symbol) & (dfBase['SMAhigh']>0)] # get the data for the symbol that is currently in loop

        latestHigh = dfSymbol['High'][dfSymbol.index[-1]] #the most recent high price


        candlesticks = go.Candlestick( # draw candlesticks
            x=dfSymbol['Date'],
            open = dfSymbol['Open'],
            close = dfSymbol['Close'],
            high = dfSymbol['High'],
            low = dfSymbol['Low']
        )

        SMA_hlc3 = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['SMAhlc3'],
            mode='lines',
            line = dict(color='black', width=2)
        )
        SMA_high = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['SMAhigh'],
            mode='lines',
            line = dict(color='black', width=1)
        )
        SMA_low = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['SMAlow'],
            mode='lines',
            line = dict(color='black', width=1)
        )
        EMA_hlc3 = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['EMAhlc3'],
            mode='lines',
            line = dict(color='blue', width=2)
        )
        EMA_high = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['EMAhigh'],
            mode='lines',
            line = dict(color='blue', width=1)
        )
        EMA_low = go.Scatter(
            x=dfSymbol['Date'],
            y=dfSymbol['EMAlow'],
            mode='lines',
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
        for index, row in dfResistanceLines.iterrows():
            """
            if (row['rankTops'] <= 5): #consider the lines only within 20%
                similarTops = int(row['similarTops'])
                avgHigh = round(row['avgHigh'],2)
                annotation_text = str(avgHigh) + ' with ' + str(similarTops) + ' times between ' + str(startDate) + ' and ' + str(endDate) + ' (' + str(row['rankTops']) + ')'
                annotation_text = ''
                fig.add_hline(y=avgHigh, row=1, col=1, annotation_text=annotation_text, annotation_position='top left', line_color='orange', line_width=1)
            """
            avgHigh = round(row['avgHigh'],2)
            if avgHigh <= (latestHigh*1.20): # ignore the lines that are 25% above the latest high
                annotation_text=''
                fig.add_hline(y=avgHigh, row=1, col=1, annotation_text=annotation_text, annotation_position='top left', line_color='orange', line_width=1)

        fig.update(layout_xaxis_rangeslider_visible=False) # to turn off the range slider at the bottom of the chart

        fig.show() # display the chart    


