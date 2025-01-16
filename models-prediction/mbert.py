from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json

# Load fine-tuned model and tokenizer
model = BertForSequenceClassification.from_pretrained("./finetuned_model")
tokenizer = BertTokenizer.from_pretrained("./finetuned_model")

# Load the JSON file
with open("captions.json", "r") as file:
    data = json.load(file)

# Extract the descriptions (assuming each description is inside 'data' key)
descriptions = [item['data'] for item in data]

# Tokenize the descriptions
inputs = tokenizer(descriptions, padding=True, truncation=True, max_length=512, return_tensors="pt")

# Make predictions
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

# Get predicted labels (class with the highest logit)
predictions = torch.argmax(logits, dim=-1)

# Define label map from your training phase
label_map = {
    0: "comedy",
    1: "educational",
    3: "lifestyle",
    2: "sports"
}

# Convert predictions to labels
predicted_labels = [label_map[pred.item()] for pred in predictions]

# Print predicted labels for each description
for description, label in zip(descriptions, predicted_labels):
    print(f"Description: {description}\nPredicted Category: {label}\n")
