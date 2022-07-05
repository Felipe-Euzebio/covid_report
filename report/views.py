from django.shortcuts import render
import requests
import csv
import datetime as dt
import traceback
from PIL import Image
from IPython.display import display
from urllib.parse import quote

# Constants
CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

# API
url = 'https://api.covid19api.com/dayone/country/brazil'


def show_report(request):

    get_api_result()
    return render(request, 'report.html')


# ----------------------------------------------------------------------------------------------------------------------
# Unrelated functions down below
# ----------------------------------------------------------------------------------------------------------------------


def get_api_result():

    try:
        response = requests.get(url)   # Get data from API
        raw_data = response.json()  # Convert to JSON
        final_data = []       # Create a list to store the data

        for obs in raw_data:    # For each observation
            final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])  # Append the data to the list

        final_data.insert(0, ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Date'])    # Insert the header to the list

        for i in range(1, len(final_data)):   # For each observation
            # noinspection PyTypeChecker
            final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y-%m-%dT%H:%M:%SZ')   # Convert the date to a datetime object

        with open('media/csv/brazil-covid19.csv', 'w') as csvfile:    # Create a CSV file
            writer = csv.writer(csvfile)    # Create a CSV writer
            writer.writerows(final_data)    # Write the data to the CSV file

        y_data_1 = []   # Create a list to store the Y-Axis 1 data (CONFIRMADOS)
        for obs in final_data[1::10]:
            y_data_1.append(obs[CONFIRMADOS])   # Append the CONFIRMADOS data to the list

        y_data_2 = []   # Create a list to store the Y-Axis 2 data (RECUPERADOS)
        for obs in final_data[1::10]:
            y_data_2.append(obs[RECUPERADOS])   # Append the RECUPERADOS data to the list

        labels = ['Confirmados', 'Recuperados']  # Create a list to store the labels

        x = []  # Create a list to store the X-Axis data (DATA)
        for obs in final_data[1::10]:
            x.append(obs[DATA].strftime('%d/%m/%Y'))    # Append the DATA data to the list and convert it to a string with the format '%d/%m/%Y'

        chart = create_chart(x, [y_data_1, y_data_2], labels, title='COVID-19 - BR: Confirmados vs. Recuperados')   # Create a chart
        chart_content = get_api_chart(chart)    # Get the chart content

        save_image('media/charts/brazil-covid19.png', chart_content)   # Save the chart content to a PNG file
        display_image('media/charts/brazil-covid19.png')  # Display the chart content

    except Exception as e:
        print(f'Error: {e}')
        print(traceback.format_exc())
        exit()


def get_datasets(y, labels):

    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })

        return datasets

    else:
        return [{
            'label': labels[0],
            'data': y
        }]


def set_title(title=''):

    if title != '':
        display = 'true'
    else:
        display = 'false'

    return {
        'title': title,
        'display': display
    }


def create_chart(x, y, labels, kind='bar', title=''):

    datasets = get_datasets(y, labels)
    options = set_title(title)

    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }

    return chart


def get_api_chart(chart):

    base_url = 'https://quickchart.io/chart'
    response = requests.get(f'{base_url}?c={str(chart)}')

    return response.content


def save_image(path, content):

    with open(path, 'wb') as image:
        image.write(content)


def display_image(path):

    img_pil = Image.open(path)
    display(img_pil)


def get_api_qrcode(link):

    text = quote(link)  # parsing the link to be able to use it in the qrcode
    base_url = 'https://quickchart.io/qr'

    response = requests.get(f'{base_url}?text={text}')
    return response.content








