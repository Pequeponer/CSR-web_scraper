import signal
import sys
import pandas as pd
from google.cloud import language_v1
from google.api_core.exceptions import InvalidArgument

# create a Google Cloud Natural Languague API Python client
client = language_v1.LanguageServiceClient.from_service_account_json(
    "path/to/api.json")


# a function which takes a block of text and returns its sentiment and magnitude
def detect_sentiment(text):
    """Detects sentiment in the text."""
    # parameters
    type_ = language_v1.Document.Type.PLAIN_TEXT
    encoding_type = language_v1.EncodingType.UTF8

    # document
    document = {"content": text, "type_": type_}

    sentiment = client.analyze_sentiment(
        request={'document': document, 'encoding_type': encoding_type}).document_sentiment

    return sentiment.score, sentiment.magnitude


# keep track of count of total comments and comments with each sentiment
count = 0
positive_count = 0

neutral_count = 0
negative_count = 0
mixed_count = 0
sentiment = []
sent_score = []
mag_score = []
text = []

# Set polarity cut-off points
high_cp = ['set', 'range', 'values']
low_cp = ['set', 'range', 'values']


# read our comments.txt file
f = pd.read_csv('path/to/full/text/comments_data.csv', encoding='utf-8')
f = f['Column_with_text_data'].tolist()

for high, low in zip(high_cp, low_cp):
    true_pos = 0
    true_neu = 0
    true_neg = 0
    false_pos = 0
    false_neu = 0
    false_neg = 0
    for line in f:
        text.append(line)
        # use a try-except block since we occasionally get language not supported errors
        # print(line)
        try:
            score, mag = detect_sentiment(line)
        except InvalidArgument as e:
            # skip the comment if we get an error
            print('Skipped 1 comment: ', e.message)
            continue

        # increment the total count
        count += 1

        # depending on whether the sentiment is positve, negative or neutral, increment the corresponding count
        if score > high:
            dum = 1
            positive_count += 1
            if dum == test:
                true_pos += 1
            else:
                false_pos += 1

            sentiment.append(dum)
            sent_score.append(score)
            mag_score.append(mag)
        elif score < low:
            dum = -1
            negative_count += 1
            if dum == test:
                true_neg += 1
            else:
                false_neg += 1
            sentiment.append(dum)
            sent_score.append(score)
            mag_score.append(mag)

        else:
            dum = 0
            neutral_count += 1
            if dum == test:
                true_neu += 1
            else:
                false_neu += 1
            sentiment.append(dum)
            sent_score.append(score)
            mag_score.append(mag)

    # calculate the proportion of comments with each sentiment

    positive_proportion = positive_count / count
    neutral_proportion = neutral_count / count
    negative_proportion = negative_count / count
    mixed_proportion = mixed_count / count

    print('Summary')
    print()
    print('Total comments analysed: {}'.format(count))
    print('Positive : {} ({:.2%})'.format(
        positive_count, positive_count / count))
    print('Negative : {} ({:.2%})'.format(
        negative_count, negative_count / count))
    print('Neutral  : {} ({:.2%})'.format(
        neutral_count, neutral_count / count))

    Sentiment = {
        'Text': text,
        'Sentiment': sentiment,
        # 'Sscore': sent_score,
        # 'Magnitude': mag_score
    }

    Confusion = {
        'TrueP': true_pos,
        'FalseP': false_pos,
        'TrueNeu': true_neu,
        'FalseNeu': false_neu,
        'TrueNeg': true_neg,
        'FalseNeg': false_neg
    }

    master = pd.DataFrame.from_dict(Sentiment, orient="index")
    master = master.transpose()
    master.to_csv(r'C:Full_sentiments.csv')
    print('archived sentiment')

    matrix = pd.DataFrame.from_dict(Confusion, orient="index")
    matrix = matrix.transpose()
    matrix.to_csv(
        rf'C:/Users/theog/Desktop/diss/Full_confusion_{high}_{low}.csv')
    print('archived confusion matrix ')
