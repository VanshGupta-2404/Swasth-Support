import pandas as pd
import numpy as np
import joblib

# Load the CSV file
csv_file = 're_train_embeds.csv'
df = pd.read_csv(csv_file)

# Convert string representations of numpy arrays to actual numpy arrays
df['short_answer_embed_numpy'] = df['short_answer_embed_numpy'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))
df['short_question_embed_numpy'] = df['short_question_embed_numpy'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))

# Save the DataFrame to a pickle file
pickle_file = 'training_data.pkl'
joblib.dump(df, pickle_file)

print(f"Data saved to {pickle_file}")
