[instructions](https://pypi.org/project/django-plotly-dash/)

## Installation
`pip install django_plotly_dash`

### settings.py
```python
INSTALLED_APPS = [
    ...
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    ...
    ]
...
X_FRAME_OPTIONS = 'SAMEORIGIN'  ## by default, this is set to DENY
```

### urls.py
```python
urlpatterns = [
    ...
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
```

### run migrate
`python manage.py migrate`

## Example
Add a .py file with the plotly app call or place it directly in the `views.py`

### plotly.py
```python
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
from django.forms.models import model_to_dict
from .models import BankAccount, BankLineItem, CreditCard, CreditCardLineItem, CreditCardPayment
from .reconcile import pd_reconcile_bank_balances

from django_plotly_dash import DjangoDash

# SIMPLE EXAMPLE app
app = DjangoDash("SimpleExample")

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')


app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                dict(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])
```

### views.py
```python
# the instantiation is sufficient, don't need to explicitly call the app
from .plotly import app
```

### budget_plotly.html
The default style is set to `height=0`, need to override it.
```html
    <style>
        #dashboard-plotly > div {
            width: 800px!important;
            height: 600px!important;
        }
    </style>
    <div id="dashboard-plotly" class="d-flex justify-content-center">
        {% load plotly_dash %}

        {% plotly_app name="BudgetDemo" %}
    </div>
```

## Other Links
[Use Figure](plotly-figure-for-plotly-dash)  
[Simple Usage](https://django-plotly-dash.readthedocs.io/en/latest/simple_use.html)  
[Basic Callbacks](https://dash.plotly.com/basic-callbacks)  
[Line Charts#Dash](https://plotly.com/python/line-charts/#what-about-dash)