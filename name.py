import pandas as pd
from openai import OpenAI


client = OpenAI()

with open("companies.txt", "r") as file:
    existing_companies = file.read().splitlines()

excel_file_path = 'Raz.xlsx'
df = pd.read_excel(excel_file_path)
companies = {}

n = len(df)
d = n
if (n > 20):
    n = 20

company = []
for i in range(d):
    company.append(df.loc[i, 'Distributor Name'])

for i in range(n):
    companies[df.loc[i, 'Distributor Name']] = df.loc[i, 'Description']

print(companies)

example = "1. Company Name - Description Of Company. Website: https://www.example.com. Country: United States"

user_prompt = f"You have {companies}. It is a companies with description. You need to find 5 new companies similar to the ones I provided. Also provide a official site of these new companies and country of foundation. Give a response like this: {example}. You need to find companies that are not here: {existing_companies}. Make description in one sentence. Display information about each company separating them '\\n\\n'."

extraction_query = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": user_prompt}], max_tokens=300).choices[0].message.content
print("I am", extraction_query)

companies_data = extraction_query.split('\n\n')
print("Companies Data: ", companies_data)
# Parse extraction_query to get new companies and their descriptions
new_companies = {}
for company_data in companies_data:
    print(company_data)
    if company_data.strip():
        # Splitting company info into parts
        company_info = company_data.split(' - ')
        print("Company Info: ", company_info)
        if len(company_info) == 2:
            name = company_info[0].split('. ')[1].strip()
            details = company_info[1].split('. ')
            print("Name", name, details)

            # Check if details has at least 3 parts
            if len(details) >= 3:
                description = details[0].strip()
                website = details[1].split('Website: ')[1].split('. ')[0].strip()
                country = details[2].split('Country: ')[1].strip()
                print("WebSite", description, website, country)
                new_companies[name] = [description, website, country]

print(new_companies)
