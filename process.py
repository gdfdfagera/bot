import pandas as pd
from openai import OpenAI

client = OpenAI()

def checkExistence(companies, country):
    new_companies = {}
    for company_data in companies:
        if company_data.strip():
            company_info = company_data.split(' - ')
            print("Company Info: ", company_info)
            if len(company_info) == 2:
                name = company_info[0].split('. ')[1].strip()
                details = company_info[1].split('. ')
                user_prompt = f"Do you know this company {name}? Answer in one word"
                extraction_query = \
                    client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_prompt}],
                                                   max_tokens=300).choices[0].message.content
                print("Query 1: ", extraction_query)
                if (extraction_query == "Yes." or extraction_query == "Yes"):
                    user_prompt = f"Is {name} company related to the medical field?? Answer in one word"
                    extraction_query = \
                        client.chat.completions.create(model="gpt-3.5-turbo",
                                                       messages=[{"role": "user", "content": user_prompt}],
                                                       max_tokens=300).choices[0].message.content
                    print("Query 2: ", extraction_query)
                    if (extraction_query == "Yes." or extraction_query == "Yes"):
                        user_prompt = f"Is the {name} company based in {country}? Answer in one word"
                        extraction_query = \
                            client.chat.completions.create(model="gpt-3.5-turbo",
                                                           messages=[{"role": "user", "content": user_prompt}],
                                                           max_tokens=300).choices[0].message.content
                        print("Query 3: ", extraction_query)
                        if extraction_query == "Yes." or extraction_query == "Yes":
                            if len(details) >= 3:
                                description = details[0].strip()
                                website = details[1].split('Website: ')[1].split('. ')[0].strip()
                                country = details[2].split('Country: ')[1].strip()
                                print("WebSite", description, website, country)
                                new_companies[name] = [description, website, country]

    return new_companies



def process_input(file_path, country):
    try:
        with open("companies.txt", "r") as file:
            existing_companies = file.read().splitlines()

        excel_file_path = file_path
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
        example = "1. 'Company Name' - 'Description Of Company'. Website: https://www.example.com. Country: United States"

        companies_result = {}

        user_prompt = f"You have {companies} and {companies_result}. It is a companies with description. You need to find 5 new companies similar to the ones I provided. Also provide a official site of these new companies and country of foundation. Here an example of your output: {example}. Just don't wrap your answer in extra quotes. You need to find companies that are not here: {existing_companies}. And don’t think that you can provide a company that is on this list simply by changing the company name. Make description in one sentence. Replace all periods in the description sentence with a comma, not counting the end of the sentence. Display information about each company separating them '\\n\\n'. If you don’t know more companies, don’t lie. No need to invent companies. You need to find companies from {country}. And again, please don’t inflate companies and their descriptions."


        while True:
            extraction_query = \
            client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_prompt}],
                                           max_tokens=300).choices[0].message.content

            print("I am", extraction_query)

            companies_data = extraction_query.split('\n\n')
            print("Companies Data: ", companies_data)
            quantity = checkExistence(companies_data, country)
            companies_result.update(quantity)
            print("Companies result: ", companies_result)
            if len(companies_result) >= 5:
                break


        print(companies_result)

        with open("companies.txt", "a+", encoding="utf-8") as file:
            for comp, _ in companies_result.items():
                if comp not in existing_companies:
                    file.write(comp + "\n")

        return companies_result
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        # You can raise an exception or return the error message based on your requirements
        raise Exception(error_message)



def process_excel(file_path):
    try:
        with open("companies.txt", "r") as file:
            existing_companies = file.read().splitlines()

        excel_file_path = file_path
        df = pd.read_excel(excel_file_path)
        companies = {}

        global last_processed_excel_info
        last_processed_excel_info = {
            "file_path": file_path,
            "existing_companies": existing_companies,
            "companies": companies,
        }

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
        example = "1. 'Company Name' - 'Description Of Company'. Website: https://www.example.com. Country: United States"

        user_prompt = f"You have {companies}. It is a companies with description. You need to find 5 new companies similar to the ones I provided. Also provide a official site of these new companies and country of foundation. Here an example of your output: {example}. Just don't wrap your answer in extra quotes. You need to find companies that are not here: {existing_companies}. And don’t think that you can provide a company that is on this list simply by changing the company name. Make description in one sentence. Replace all periods in the description sentence with a comma, not counting the end of the sentence. Display information about each company separating them '\\n\\n'. If you don’t know more companies, don’t lie. No need to invent companies."

        extraction_query = \
        client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_prompt}],
                                       max_tokens=300).choices[0].message.content
        print("I am", extraction_query)

        companies_data = extraction_query.split('\n\n')
        print("Companies Data: ", companies_data)

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

                    if len(details) >= 3:
                        description = details[0].strip()
                        website = details[1].split('Website: ')[1].split('. ')[0].strip()
                        country = details[2].split('Country: ')[1].strip()
                        print("WebSite", description, website, country)
                        new_companies[name] = [description, website, country]

        print(new_companies)

        with open("companies.txt", "a+", encoding="utf-8") as file:
            for comp, _ in new_companies.items():
                if comp not in existing_companies:
                    file.write(comp + "\n")

        return new_companies, last_processed_excel_info
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        # You can raise an exception or return the error message based on your requirements
        raise Exception(error_message)