from openai import OpenAI
import dotenv
import os

def getAPI(name): #get API key from .env
    dotenv.load_dotenv()
    return os.getenv(name)

def getclient(API_KEY,base_url): #get client for API calls
    client = OpenAI(api_key=API_KEY, base_url= base_url)
    return client

def available_models(client): # show and select available models
    models = client.models.list()
    print(models)
    i = 0
    for model in models:
        i = i + 1
        print(f"{i}",model.id)
    try:
        model_no = int(input("Select through model number : "))
        os.system("clear")
        return list(models)[model_no - 1].id
    except (ValueError, IndexError):
        return list(models)[0].id

def main():
    API_KEY = getAPI("GROQ_API")
    client = getclient(API_KEY,base_url = "https://api.groq.com/openai/v1")
    model= available_models(client)
    
    input_history = [{"role": "system", "content": """You are a helpful assistant. that help in planning a trip to a city or coutry according to the family members, days and budget for the trip,
        if Budget is too low for the trip, show the user a message that the budget is too low and suggest them to increase the budget or 
                      decrease the number of days or family members. If the user has any specific preferences for the trip, such as activities or attractions they want to visit, take that into account when planning the trip. Provide a detailed itinerary for the trip, including recommended accommodations, transportation options,
                       and activities to do in the city or country. Make sure to consider the user's preferences and
                       budget when planning the trip.ask for each requirement one by one and if the user has not provided any requirement, ask the user to provide that information before planning the trip.
                      if the any requirement is missing from the user,ask the user to provide that information before planningthe trip
                      if the user enter something that is not related to the trip planning, respond with a message that you are here to help in planning the trip and ask them to provide the required information for planning the trip.
                      """},             # set the system promt
        {"role" : "user", "content" : "I want to plan a trip to Paris for 4 family members for 5 days with a budget of $2000. I want to visit the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral. Can you help me plan this trip?"},
        {"role": "assistant", "content": """Sure! I can help you plan your trip to Paris. Based on your requirements, here is a suggested itinerary for your 5-day trip: \n 
         Day 1: Arrival in Paris and check-in at your accommodation. \n
          Day 2: Visit the Eiffel Tower in the morning, followed by a visit to the Louvre Museum"""}
    ]
    print("type Quit or Exit to stop the conversation")
    while True:
        prompt = input("PROMPT : ")
        if not prompt:
            continue
        elif prompt.lower() == "quit" or prompt.lower() == "exit":
            break
        input_history.append({"role" : "user", "content" : prompt})
        response = client.chat.completions.create(
            model= model,
            messages= input_history)
        assistant = {"role": "assistant", "content": response.choices[0].message.content}
        input_history.append(assistant)
        print("RESPONSE : \n",response.choices[0].message.content)

        

    
main()