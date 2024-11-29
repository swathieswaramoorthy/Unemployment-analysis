# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file1_path = 'Unemployment in India.csv'
file2_path = 'Unemployment_Rate_upto_11_2020.csv'

data1 = pd.read_csv(file1_path)
data2 = pd.read_csv(file2_path)

data1.columns = data1.columns.str.strip()
data2.columns = data2.columns.str.strip()

# Drop duplicate or unnecessary columns
if 'Region.1' in data2.columns:
    data2 = data2.drop(columns=['Region.1'])

# Ensure consistent column names
common_columns = ['Region', 'Date', 'Frequency', 'Estimated Unemployment Rate (%)', 
                  'Estimated Employed', 'Estimated Labour Participation Rate (%)']
data1 = data1[common_columns]
data2 = data2[common_columns + ['longitude', 'latitude']]  # Include extra columns from data2

# Convert 'Date' columns to datetime format
data1['Date'] = pd.to_datetime(data1['Date'])
data2['Date'] = pd.to_datetime(data2['Date'])

# Step 2: Merge the Datasets
# Combine both datasets into one, ignoring duplicates
merged_data = pd.concat([data1, data2], ignore_index=True).drop_duplicates()

# Step 3: Basic Data Analysis
# Check for missing values
print("Missing Values:\n", merged_data.isnull().sum())

# Fill missing values (if any)
merged_data.fillna(method='ffill', inplace=True)

# Display merged dataset info
print("\nMerged Dataset Info:")
print(merged_data.info())

# Step 4: Data Visualization
# Unemployment rate trends over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=merged_data, x='Date', y='Estimated Unemployment Rate (%)', hue='Region')
plt.title('Unemployment Rate Over Time by Region')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

avg_unemployment_by_region = merged_data.groupby('Region')['Estimated Unemployment Rate (%)'].mean()

plt.figure(figsize=(10, 6))
avg_unemployment_by_region.sort_values().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Average Unemployment Rate by Region')
plt.ylabel('Unemployment Rate (%)')
plt.xlabel('Region')
plt.tight_layout()
plt.show()

avg_participation_rate = merged_data.groupby('Region')['Estimated Labour Participation Rate (%)'].mean()

plt.figure(figsize=(10, 6))
avg_participation_rate.sort_values().plot(kind='bar', color='orange', edgecolor='black')
plt.title('Average Labour Participation Rate by Region')
plt.ylabel('Labour Participation Rate (%)')
plt.xlabel('Region')
plt.tight_layout()
plt.show()

cleaned_file_path = 'cleaned_unemployment_data.csv'
merged_data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned dataset saved to {cleaned_file_path}")

