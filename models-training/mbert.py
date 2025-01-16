import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_excel('instagram_post_classification_with_extended_darija.xlsx')

# Split data into texts and labels
texts = df['text'].tolist()
labels = df['label'].tolist()

# Create a label-to-id mapping (mapping the text labels to unique integers)
label_map = {label: idx for idx, label in enumerate(set(labels))}
print(label_map)
# Convert labels to integers using the label_map
numeric_labels = [label_map[label] for label in labels]

# Initialize tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# Tokenize texts
encodings = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors='pt')

# Convert numeric labels to tensor
labels_tensor = torch.tensor(numeric_labels)

# Split dataset into training and validation sets
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels_tensor, test_size=0.1)

# Tokenize the datasets
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512, return_tensors='pt')
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512, return_tensors='pt')

# Ensure the dataset returns dictionaries with the proper keys
train_dataset = TensorDataset(train_encodings['input_ids'], train_encodings['attention_mask'], train_labels)
val_dataset = TensorDataset(val_encodings['input_ids'], val_encodings['attention_mask'], val_labels)

# Convert TensorDataset to dictionary format required by Trainer
def collate_fn(batch):
    input_ids = torch.stack([item[0] for item in batch])
    attention_mask = torch.stack([item[1] for item in batch])
    labels = torch.stack([item[2] for item in batch])
    return {'input_ids': input_ids, 'attention_mask': attention_mask, 'labels': labels}

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=8,   # batch size for training
    per_device_eval_batch_size=8,    # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
)

# Initialize model
model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=len(label_map))

# Initialize Trainer
trainer = Trainer(
    model=model,                         # the model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=val_dataset,            # evaluation dataset
    data_collator=collate_fn             # provide custom collate function
)

# Train the model
trainer.train()


# # Save the model after training
trainer.save_model('./finetuned_model')
# Save the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
tokenizer.save_pretrained('./finetuned_model')

