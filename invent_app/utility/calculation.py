import calendar
from datetime import datetime

def get_month_list(year):
    month_names = []
    for month in range(1, 13):
        month_names.append(calendar.month_name[month])
    return month_names

def get_current_month_dates(year,month):
    num_days = calendar.monthrange(year=year, month=month)[1]
    dates_list = [day for day in range(1, num_days + 1)]
    return dates_list



def option_dictionary(series,title,xaxis,yaxis,month):
    options = {
        "series": series,
        "chart": {
            "height": 350,
            "type": 'line',
            "dropShadow": {
                "enabled": True,
                "color": '#000',
                "top": 18,
                "left": 7,
                "blur": 10,
                "opacity": 0.2
            },
            "toolbar": {
                "show": False
            }
        },
        "colors": ['#77B6EA', '#545454', '#00A36C'],
        "dataLabels": {
            "enabled": True
        },
        "stroke": {
            "curve": 'smooth'
        },
        "title": {
            "text": title,
            "align": 'left'
        },
        "grid": {
            "borderColor": '#e7e7e7',
            "row": {
                "colors": ['#f3f3f3', 'transparent'],
                "opacity": 0.5
            }
        },
        "markers": {
            "size": 1
        },
        "xaxis": {
            "categories": xaxis,
            "title": {
                "text": month
            }
        },
        "yaxis": {
            "title": {
                "text": yaxis
            },
            "min": 0,
        },
        "legend": {
            "position": 'top',
            "horizontalAlign": 'right',
            "floating": True,
            "offsetY": -25,
            "offsetX": -5
        }
    }
    return options
