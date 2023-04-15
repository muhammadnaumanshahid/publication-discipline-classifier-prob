import pandas as pd
from collections import defaultdict

# Read the keywords from the text files into a dictionary
def read_keywords(file_name):
    with open(file_name, 'r') as f:
        keywords = f.read().split(', ')
    return keywords

# Classify the discipline of a publication based on the title and abstract
def classify_discipline(title, abstract, disciplines):
    max_matches = 0
    discipline_result = "Unknown"
    total_keywords = sum([len(keywords) for keywords in disciplines.values()])

    for discipline, keywords in disciplines.items():
        matches = sum([1 for keyword in keywords if keyword.lower() in title.lower() or keyword.lower() in abstract.lower()])
        if matches > max_matches:
            max_matches = matches
            discipline_result = discipline

    probability = max_matches / total_keywords if total_keywords > 0 else 0
    return discipline_result, probability

# Read the keywords for each discipline
disciplines = {
    'Business': read_keywords('business.txt'),
    'Computer Science': read_keywords('computer_science.txt'),
    'Engineering': read_keywords('engineering.txt'),
    'Social Science': read_keywords('social_science.txt'),
    'Healthcare': read_keywords('healthcare.txt'),
    'Economics': read_keywords('economics.txt'),
    'Law': read_keywords('law.txt')
}

# Read the publications_data.xlsx file
df = pd.read_excel('publications_data.xlsx')

# Classify the discipline and probability for each row in the DataFrame
df[['discipline', 'probability']] = df.apply(lambda row: classify_discipline(row['title'], row['abstract'], disciplines), axis=1, result_type="expand")

# Save the result to a new Excel file
df.to_excel('classified_publications_data_with_probability.xlsx', index=False)
