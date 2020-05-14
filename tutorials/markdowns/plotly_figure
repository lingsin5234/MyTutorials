Store the figure in a variable `fig` before calling it from `dcc.Graph`, this way, the `layout.template` is processed

### plotly.py
```python
# construct the graph
fig = go.Figure()

for i in df.account_name.unique():
    fig.add_trace(go.Scatter(
        x=df[df['account_name'] == i]['date_stamp'],
        y=df[df['account_name'] == i]['amount'],
        text=df[df['account_name'] == i]['Trans_Type'],
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name=i
    ))

fig.layout = dict(
        xaxis={'type': 'date', 'title': 'Date'},
        yaxis={'title': 'Spending / Earnings'},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest',
        template='plotly_dark'
    )

# show the graph
budget_demo.layout = html.Div([
    dcc.Graph(
        id='budget_demo',
        figure=fig
    )
])
```