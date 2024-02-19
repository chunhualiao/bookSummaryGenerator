from langchain_openai import ChatOpenAI
import json

# langchain_openai.chat_models.base.ChatOpenAI
# TODO: specify MODEL ID? 
llm = ChatOpenAI()

# langchain_core.messages.ai.AIMessage
# result = llm.invoke("how can langsmith help with testing?")
#print (result.content)

# prompt template
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

"""
In standard Python usage, the bitwise OR operator is not designed to work with objects that aren't integers. If `prompt` and `llm` are indeed not integers, then it suggests that one or both of these variables represent custom objects that have overridden the `__or__` method, which is the special method in Python that corresponds to the bitwise OR operator.
When the `__or__` method is overridden in a custom class, the `|` operator can be used to implement any operation between instances of the class. 
For example, if `prompt` and `llm` are instances of a class that models a chainable operation or a pipeline, the `|` operator could be used to combine these operations into a single chained operation, which is then stored in the `chain` variable. This pattern is sometimes used in Python to create a fluent interface that allows for the chaining of methods or functions in a more readable manner.
"""
#chain = prompt | llm   # langchain_core.runnables.base.RunnableSequence

# key value pairs for the prompt
# langchain_core.messages.ai.AIMessage
# result = chain.invoke({"input": "how can langsmith help with testing?"})

#print (result.content)

# add a simple output parser to convert the chat message to a string.
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

# the universal chain for invoking LLM
chain = prompt | llm | output_parser

billionaires_filename = "billionaires_data.txt"
name_list = None 
from pathlib import Path

if Path(billionaires_filename).exists():
    print (f"File {billionaires_filename} already exists, skip this step")
else:  
    # Painpoint: the prompt must be explicit about the output format, tried a few variants to finally get what I wanted.
    result = chain.invoke({"input": "Please list 50 self made billionaires in the world. Save give their names in a json format, using a key billionaires and a value listing only names:"})

    # TODO: also need error handling
    # I\'m sorry, but I cannot provide a list of 100 self-made billionaires as it would be a lengthy and constantly changing list. However, .... 
    # sometimes the results are not json, need sanity check!
    # also the format is not consistent: self_made_billionairs: [{name1: value1, name2: value2, ...}]
    """
    {
    "billionaires": [
    "Jeff Bezos",
    "Elon Musk",
    "Bernard Arnault",
    "Bill Gates",
    "Mark Zuckerberg",
    "Warren Buffett",
    "Larry Page",
    "Sergey Brin",
    "Larry Ellison",
    "Mukesh Ambani"
    ]
    }
    """
    print(result)
    data =json.loads(result)

    # Convert the dictionary back to a JSON string for storage
    # Use json.dumps(data, indent=4) for a prettified JSON format
    json_data_to_store = json.dumps(data, indent=4)
    # Open a text file for writing
    with open(billionaires_filename, 'w') as file:
        # Write the JSON data to the file
        file.write(json_data_to_store)


# at this point, the billionaires_data.txt file is created or exists.
# read the billionaires_data.txt file
with open(billionaires_filename, 'r') as file:
    # Read the contents of the file
    data = json.load(file)    
    print("Data has been loaded from 'billionaires_data.txt'")
    name_list = data['billionaires']
    print (name_list)

counter = 1
for name in name_list:
    # Open a text file for writing
    # using 3 digits string as a prefix
    counter_prefix_str = str(counter).zfill(3)
    # name has spaces in it, add a hyphen
    hyphen_name = name.replace(" ", "-")
    file_name = counter_prefix_str+hyphen_name+'_books.txt'
    
    # if the file already exists, skip this name
    if Path(file_name).exists():
        print(f"{file_name} already exists, skip this name")
        counter += 1
        continue
    
    prompt = "Please list up to 25 books recommended by " + name + ". Give the book list in a json format, using a key books and a value listing only book names:"
    result = chain.invoke({"input": prompt})
    
    # using load and dump to check the result is really json format
    data =json.loads(result)

    # Use json.dumps(data, indent=4) for a prettified JSON format
    json_data_to_store = json.dumps(data, indent=4)

    with open(file_name, 'w') as file:
        # Write the JSON data to the file
        file.write(json_data_to_store)
    counter += 1  

# make it better to use a retrieval chain to obtain information from forbes website listing richest billionaires.
#from langchain_community.document_loaders import WebBaseLoader
#loader = WebBaseLoader("https://docs.smith.langchain.com")
#docs = loader.load()