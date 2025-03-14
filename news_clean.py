import re

# Read the text file
with open("scraped_news.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Regular expression to remove URLs
text_cleaned = re.sub(r"http[s]?://\S+|www\.\S+", "", text)

# Save the cleaned text
with open("cleaned_text.txt", "w", encoding="utf-8") as file:
    file.write(text_cleaned)

print("URLs removed successfully!")
