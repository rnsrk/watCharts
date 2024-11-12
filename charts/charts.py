import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

def bar_chart(data, title):
    data = data.str.split(';').explode().value_counts()
    fig, ax = plt.subplots(figsize=(12,6))
    palette = sns.color_palette("husl", len(data))
    sns.barplot(x=data.index, y=data.values, ax=ax, hue=data.index, palette=palette, legend=False)
    ax.set_xlabel('Answer')
    ax.set_ylabel('Count')

    # Rotate the x-axis labels and set their horizontal alignment
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
        tick.set_horizontalalignment('right')
        tick.set_fontsize(12)

    fig.tight_layout()

    img = io.BytesIO()
    fig.savefig(img, format='png', dpi=300, bbox_inches='tight', pad_inches=0.5)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

def bar_chart_with_special_legend(data, title, scale='recommendation'):
    if scale == 'recommendation':
        data = data.map({1:'not likely', 2:'less likely', 3:'not sure', 4:'more likely', 5:'definitely'})

    # create a value counts series
    data_counts = data.value_counts()

    fig, ax = plt.subplots(figsize=(12,6))
    palette = sns.color_palette("husl", 5)
    sns.barplot(x=data_counts.index, y=data_counts.values, ax=ax, hue=data_counts.index, palette=palette)
    ax.set_xlabel('Answer')
    ax.set_ylabel('Count')

    # set y-axis to only have integer values
    ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))

    # Rotate the x-axis labels and set their horizontal alignment
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
        tick.set_horizontalalignment('right')
        tick.set_fontsize(12)

    fig.tight_layout()

    img = io.BytesIO()
    fig.savefig(img, format='png', dpi=300, bbox_inches='tight', pad_inches=0.5)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

def pie_chart(data, title):
    data = data.str.split(';').explode().value_counts()
    fig, ax = plt.subplots(figsize=(12,6))
    ax.pie(data.values, labels=data.index, autopct='%1.1f%%')
    fig.tight_layout()
    img = io.BytesIO()
    fig.savefig(img, format='png', dpi=300, bbox_inches='tight', pad_inches=0.5)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

def point_chart(data, title):
    # Count the occurrences of each value

    # Map the x-axis values to the appropriate string
    data = data.map({1:'not important', 2:'less important', 3:'important', 4:'more important', 5:'mandatory'})

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot your data
    for answer, value in data.items():
        ax.plot([value], [answer], marker='o')

    # Set the x-axis ticks and labels
    ax.set_xticks(list(set(data.values)))
    ax.set_xticklabels(list(set(data.values)), rotation=45)

    # Set the y-axis limits to remove the axis
    ax.set_yticks(list(data.keys()))

    # Set the font size of the y-axis
    for tick in ax.get_yticklabels():
        tick.set_fontsize(9)

    fig.tight_layout()
    img = io.BytesIO()
    fig.savefig(img, format='png', dpi=300, bbox_inches='tight', pad_inches=0.5)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

