# 一、TextBlob情感分析

from textblob import TextBlob

def get_sentiment(text):
    analysis = TextBlob(str(text))
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

df["sentiment"] = df["comment"].apply(get_sentiment)
print(df["sentiment"].value_counts())  # 统计正负面评论数量


# 二、生成词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# 拼接所有文本
text = " ".join(str(comment) for comment in df["comment"])

# 生成词云
wordcloud = WordCloud(stopwords=stop_words, width=800, height=400, background_color="white").generate(text)

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()



# 三、关键词提取
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words="english", max_features=10)  # 取10个最重要的词
tfidf_matrix = vectorizer.fit_transform(df["comment"].dropna())
API部署
keywords = vectorizer.get_feature_names_out()
print("Top Keywords:", keywords)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    comment = data.get("comment", "")
    sentiment = sentiment_model(comment)[0]["label"]
    return jsonify({"comment": comment, "sentiment": sentiment})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# （Flask API,可用POST调用，感觉调用有问题，可尝试）
# 深度学习，预测情绪