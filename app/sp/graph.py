import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
import io
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import os
import numpy as np

def plot(data, gtype, name=""):
    if len(data) == 0:
        gtype = "empty"
    dates = [ d['_id'] for d in data ]
    ping = [ d['ping'] for d in data ]
    download = [ d['download'] for d in data ]
    upload = [ d['upload'] for d in data ]
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(plt.MaxNLocator(7))
    if gtype == "ping":
        title = "Ping - {0} - Min: {1} Max: {2} Avg: {3}".format(name, round(min(ping), 2), round(max(ping), 2), round(sum(ping)/len(ping), 2))
        ax.title.set_text(title)
        ax.xaxis.label.set_text('Date')
        ax.yaxis.label.set_text('Ping (ms)')
        ax.plot(dates, ping)
    elif gtype == "download":
        title = "Download - {0} - Min: {1} Max: {2} Avg: {3}".format(name, round(min(download), 2), round(max(download), 2), round(sum(download)/len(download), 2))
        ax.title.set_text(title)
        ax.xaxis.label.set_text('Date')
        ax.yaxis.label.set_text('download (Mb/s)')
        ax.plot(dates, download)
    elif gtype == "upload":
        title = "Upload - {0} - Min: {1} Max: {2} Avg: {3}".format(name, round(min(upload), 2), round(max(upload), 2), round(sum(upload)/len(upload), 2))
        ax.title.set_text(title)
        ax.xaxis.label.set_text('Date')
        ax.yaxis.label.set_text('upload (Mb/s)')
        ax.plot(dates, upload)
    elif gtype == "empty":
        title = "No Results Found"
        ax.title.set_text(title)
    elif gtype == "all":
        title = "All - {0} - ({1} Samples)".format(name, len(dates))
        ax.title.set_text(title)
        ax.xaxis.label.set_text('Date')
        ax.plot(dates, ping, label="Ping")
        ax.plot(dates, download, label="Download")
        ax.plot(dates, upload, label="Upload")
        ax.legend()
    else:
        return None
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return output.getvalue()


def plot_upload(timeframe):
    data = get_data(timeframe)
    name = timeframe
    dates = []
    upload = []
    for tst in data:
        upload.append(tst['upload'])
        dates.append(tst['dates'])
    dates, upload = zip(*sorted(zip(dates, upload)))
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(plt.MaxNLocator(7))
    title = "upload - {0} - Min: {1} Max: {2} Avg: {3}".format(name, round(min(upload), 2), round(max(upload), 2), round(sum(upload)/len(upload), 2))
    ax.title.set_text(title)
    ax.xaxis.label.set_text('Date')
    ax.yaxis.label.set_text('upload (Mb/s)')
    ax.plot(dates, upload)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return output.getvalue()

def plot_all(timeframe):
    data = get_data(timeframe)
    name = timeframe
    dates = []
    ping = []
    upload = []
    download = []
    for tst in data:
        ping.append(tst['ping'])
        dates.append(tst['dates'])
        upload.append(tst['upload'])
        download.append(tst['download'])
    dates, ping, download, upload = zip(*sorted(zip(dates, ping, download, upload)))
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(plt.MaxNLocator(7))
    title = "All - {0} - ({1} Samples)".format(name, len(dates))
    ax.title.set_text(title)
    ax.xaxis.label.set_text('Date')
    ax.plot(dates, ping, label="Ping")
    ax.plot(dates, download, label="Download")
    ax.plot(dates, upload, label="Upload")
    ax.legend()
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return output.getvalue()

#plot_ping(all_time, "all_time")
#plot(this_month, "this_month")
#plot(today, "today")
#data = plot_ping(hour(), "this_hour")

#print(data)
