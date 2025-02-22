import plotly.graph_objects as go
import plotly.express as px

def create_time_series_plot(df, chart_type):
    """
    Create time series visualization using Plotly
    """
    if chart_type == "Line Chart":
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['usage'],
                mode='lines',
                name='Water Usage',
                line=dict(color='#2E86C1', width=2)
            )
        )
    else:  # Bar Chart
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['date'],
                y=df['usage'],
                name='Water Usage',
                marker_color='#2E86C1'
            )
        )
    
    fig.update_layout(
        title='Water Usage Over Time',
        xaxis_title='Date',
        yaxis_title='Usage (gallons)',
        hovermode='x unified',
        showlegend=False,
        template='plotly_white'
    )
    
    return fig

def create_usage_histogram(df):
    """
    Create histogram of usage distribution
    """
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df['usage'],
            nbinsx=30,
            marker_color='#2E86C1'
        )
    )
    
    fig.update_layout(
        title='Usage Distribution',
        xaxis_title='Usage (gallons)',
        yaxis_title='Frequency',
        showlegend=False,
        template='plotly_white'
    )
    
    return fig
