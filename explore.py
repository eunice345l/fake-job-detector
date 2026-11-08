import pandas as pd

df = pd.read_csv("data/fake_job_postings.csv")

print("Shape (rows, columns):", df.shape)
print()
print("Columns:")
print(list(df.columns))
print()
print("Real (0) vs fake (1):")
print(df["fraudulent"].value_counts())
print()
print("Share of fake postings: {:.1%}".format(df["fraudulent"].mean()))
print()
print("Missing values per column:")
print(df.isnull().sum())

text_cols = ["title", "company_profile", "description", "requirements", "benefits"]
df["text"] = df[text_cols].fillna("").agg(" ".join, axis=1)
df["text_length"] = df["text"].str.len()
print()
print("Average text length, real vs fake:")
print(df.groupby("fraudulent")["text_length"].mean())

print()
print("One fake posting:")
print(df[df["fraudulent"] == 1]["text"].iloc[0][:500])