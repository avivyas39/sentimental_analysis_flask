import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import os

def analyze_sentiment(filepath, output_folder):
    """
    Perform sentiment analysis on the given CSV file and generate a bar chart.

    Args:
        filepath (str): Path to the uploaded CSV file.
        output_folder (str): Folder to save the sentiment plot.

    Returns:
        tuple: DataFrame with sentiment analysis results and the plot file path.
    """
    # Read the CSV file
    df = pd.read_csv(filepath)
    if df.empty or df.shape[1] < 1:
        raise ValueError("CSV must contain at least one column with text for sentiment analysis.")

    # Perform sentiment analysis
    sentiments = []
    for text in df.iloc[:, 0]:
        analysis = TextBlob(str(text))
        polarity = analysis.sentiment.polarity
        sentiments.append(
            'Positive' if polarity > 0 else
            'Negative' if polarity < 0 else
            'Neutral'
        )

    # Add results to the DataFrame
    df['Sentiment'] = sentiments

    # Generate a bar chart
    sentiment_counts = df['Sentiment'].value_counts()
    plt.figure(figsize=(10, 6))
    colors = ['#76c7c0', '#f57c00', '#90caf9']  # Customize colors
    sentiment_counts.plot(kind='bar', color=colors, alpha=0.8, edgecolor='black')

    plt.title('Sentiment Distribution', fontsize=16)
    plt.xlabel('Sentiment', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the plot
    plot_filename = 'sentiment_plot.png'
    plot_path = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_path)
    plt.close()

    return df, plot_path
