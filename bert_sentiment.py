from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load FinBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def calculate_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return {
        'positive': probs[0][0].item(),
        'negative': probs[0][1].item(),
        'neutral': probs[0][2].item(),
        'compound': probs[0][0].item() - probs[0][1].item()
    }

def analyze_sentiment(file_path):
    with open(file_path, 'r') as file:
        full_text = file.read()

    articles = [art.strip() for art in full_text.split("================================================================================") if art.strip()]
    
    # Analyze individual articles
    article_results = []
    for i, article in enumerate(articles, 1):
        sentiment = calculate_sentiment(article)
        article_results.append({
            'article_number': i,
            'sentiment': sentiment,
            'excerpt': article[:100] + "..."  # Show first 100 chars as preview
        })
    
    # Analyze aggregated articles
    avg_sentiment = {
        'positive': sum(art['sentiment']['positive'] for art in article_results) / len(article_results),
        'negative': sum(art['sentiment']['negative'] for art in article_results) / len(article_results),
        'neutral': sum(art['sentiment']['neutral'] for art in article_results) / len(article_results),
        'compound': sum(art['sentiment']['compound'] for art in article_results) / len(article_results)
    }
    
    # Analyze full text
    full_text_sentiment = calculate_sentiment(full_text)
    
    return {
        'individual_articles': article_results,
        'average_sentiment': avg_sentiment,
        'full_text_sentiment': full_text_sentiment
    }

# Example usage and visualization
results = analyze_sentiment("zomato.txt")

# Print individual article analysis
print("📰 Individual Article Analysis:")
for art in results['individual_articles']:
    print(f"\nArticle #{art['article_number']}")
    print(f"Preview: {art['excerpt']}")
    print(f"Positive: {art['sentiment']['positive']:.2f}")
    print(f"Negative: {art['sentiment']['negative']:.2f}")
    print(f"Neutral: {art['sentiment']['neutral']:.2f}")
    print(f"Compound: {art['sentiment']['compound']:.2f}")

# Print aggregated results
print("\n📊 Aggregated Analysis:")
print(f"Average Positive Sentiment: {results['average_sentiment']['positive']:.2f}")
print(f"Average Negative Sentiment: {results['average_sentiment']['negative']:.2f}")
print(f"Average Neutral Sentiment: {results['average_sentiment']['neutral']:.2f}")
print(f"Average Compound Score: {results['average_sentiment']['compound']:.2f}")

# Print full text analysis
print("\n📈 Full Text Analysis:")
print(f"Positive: {results['full_text_sentiment']['positive']:.2f}")
print(f"Negative: {results['full_text_sentiment']['negative']:.2f}")
print(f"Neutral: {results['full_text_sentiment']['neutral']:.2f}")
print(f"Compound: {results['full_text_sentiment']['compound']:.2f}")

# Interpretation helper
def interpret(score):
    if score > 0.3: return "Strong Bullish"
    if score > 0.1: return "Moderate Bullish"
    if score < -0.3: return "Strong Bearish"
    if score < -0.1: return "Moderate Bearish"
    return "Neutral"

print("\n🧠 Expert Interpretation:")
print(f"Article Average: {interpret(results['average_sentiment']['compound'])}")
print(f"Full Text: {interpret(results['full_text_sentiment']['compound'])}")
