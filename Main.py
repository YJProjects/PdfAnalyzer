# %%
import PyPDF2 as pdf

PDF = open('APPLE.pdf' , 'rb')

pages = pdf.PdfReader(PDF).pages

raw_text = ''

for i in range(len(pages)):
    page = pages[i]
    raw_text += page.extract_text()

# %%
#Splitting raw text


def chunks(text , size):
    split_text = []
    i = 0
    for z in range(10 , len(text), size):
        temp = text[i:z]
        split_text.append(temp.replace('\n' , ''))
        i = z

    return(split_text)


split_text = chunks(text=raw_text , size = 300)

# %%
#Creating Vector Database

import chromadb
from chromadb.utils import embedding_functions
import openai
import os

openai.api_key = os.environ["KEY"]



client = chromadb.Client()  

embedding_model = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002" , )

text_embeddings = embedding_model(split_text)
#Creating Ids

id = []
for i in range(len(split_text)):
    id.append(str(i))
    


# %%
collection = client.get_or_create_collection(name = "APPLE.pdf" , embedding_function=embedding_model) 

collection.add(
    documents=split_text,
    embeddings=text_embeddings,
    ids = id
)


# %%
results = collection.query(
    query_texts=["What is apple's 2023 revenue revenue"],
    n_results=4
)



# %%
context = results["documents"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are a helpful assistant and you will answer the question given by the user in a breif 30 - 70 words based on the given context marked by triple quotes.Do not make anything up. After every chat say thank you for asking the question. If you do not know the answer based on the context say 'I do not know the answer'. context : {context}"},
        {"role": "user", "content": "What is apple's revenue"},
    ]
)

# %%
print(response['choices'][0]['message']['content'])

#BACKEND COMPLETE