import json
import sys
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Replace these values with your actual API keys
HF_API_TOKEN = "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"
CLAUDE_API_KEY = "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"

embedder = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_API_TOKEN, model_name="sentence-transformers/all-MiniLM-l6-v2"
)
chroma_client = Chroma(
    embedding_function=embedder,
    persist_directory='./database/chroma'
)
claude = Anthropic(api_key=CLAUDE_API_KEY)

def claude_completion(prompt, model_name="claude-instant-1", max_tokens=500):
    advisor_prompt = f"{HUMAN_PROMPT} " + str(prompt) + f" {AI_PROMPT}"
    res = claude.completions.create(
        model=model_name,
        max_tokens_to_sample=max_tokens,
        prompt=advisor_prompt
    )
    return res.completion

def parse_advisor_response(response):
    try:
        # Modify this part based on the actual structure of your response
        advisor_response = response.strip()
        return advisor_response
    except Exception as e:
        print(f"Unexpected error in parse_advisor_response: {str(e)}")
        return None

def call_anthropic_chatbot(prompt):
    try:
        # Use Anthropic to complete the prompt
        response = claude_completion(prompt)
        
        # Parse the response to extract the chatbot's advice
        chatbot_response = parse_advisor_response(response)

        return chatbot_response
    except Exception as e:
        print(f"Error in call_anthropic_chatbot: {str(e)}")
        return None


# Map user commands to their respective outputs
command_outputs = {
    "help": "advisorbot> The available commands are help, help <cmd>, prod, min, max, matchStats, avg, predict, VAR, SD, skewness, time, step, exit.",
    "prod": "advisorbot> Products:\nETH/BTC\nDOGE/BTC\n...",
    "min": "advisorbot> The min ask for ETH/BTC is 1.0",
    "max": "advisorbot> The max ask for ETH/BTC is 1.0",
    "matchStats": "advisorbot> ETH/BTC - 5\nDOGE/BTC - 3\n...",
    "avg": "advisorbot> The average ETH/BTC ask price over the last 10 timestamps was 1.0",
    "predict": "advisorbot> The average ETH/BTC max bid price over the last 10 timesteps was 1.0",
    "VAR": "advisorbot> The Variance for product ETH/BTC bid price in the current timestep is 1.0",
    "SD": "advisorbot> The Standard Deviation for product ETH/BTC bid price in the current timestep is 1.0",
    "skewness": "advisorbot> The Skewness for product ETH/BTC bid price in the current timestep is 1.0",
    "time": "advisorbot> 2020/03/17 17:01:24",
    "step": "advisorbot> now at 2020/03/17 17:01:30",
    "exit": "advisorbot> exit the advisorbot program",
    # Add more commands and their outputs as needed
}

# Command functions (replace with actual functions or text)
command_functions = {
    "help": "printHelp",
    "products": "listProducts",
    "min": "findMin",
    "max": "findMax",
    "matchStats": "printSuccessfulMatches",
    "average": "avg",
    "predict": "predict",
    "variance": "variance",
    "standard devialtion": "standardDeviation",
    "skewness": "skewness",
    "time": "printCurrentTimeframe",
    "step": "gotoNextTimeframe",
    "exit": "exitProgram",
    # Add more commands and functions as needed
}

def main():
    # Check if the user provided a command-line argument
    if len(sys.argv) < 2:
        print("Please provide a user command.")
        return

    # User command is the second command-line argument
    user_command = sys.argv[1]

    # Provide a prompt with a placeholder for the query in the answer
    prompt = f"""
    Command Context: User is making a query '{user_command}'. Make sure to only reply with the name of the command function from the list along with the respective arguments (where necessary).
    {command_outputs}
    Available Commands and Functions:
    {command_functions}
    User Command: {user_command}
    Command Functions: {command_functions}

    Example User Command : Hi can you help me with the commands.
    Output: printHelp

    Example User Command : Hi what is the min ask for ETH/BTC
    Output: findMin, BTC/ETH, ask, min

    Example User Command : Hi what is the max ask for ETH/BTC
    Output: findMax, BTC/ETH, ask, max

    Example User Command : Hi what is the average ETH/BTC ask price over the last 10 timesteps
    Output: avg, ETH/BTC, ask, 10

    Example User Command : Hi can you predict the max ETH/BTC bid price
    Output: predict, ETH/BTC, bid, 10

    Example User Command : What is the variance for the product ETH/BTC bid price
    Output: variance, ETH/BTC, bid

    Example User Command : What is the Standard Deviation for the product ETH/BTC bid price
    Output: standardDeviation, ETH/BTC, bid
    
    Example User Command : What is the Skewness for the product ETH/BTC bid price
    Output: pythonOutput

    Example User Command : Can you show the current timestep or timeframe we are in
    Output: printCurrentTimeframe

    Example User Command : Can you move to the next timestep or timeframe
    Output: gotoNextTimeframe

    Example User Command : I need to exit the program
    Output: exitProgram
    
    Context: If user asks any other question not related then just reply as show below.

    Example User Command: What is my or your name
    Output: No answer

    """

    # Call Anthropic chatbot API with the user's command
    chatbot_response = call_anthropic_chatbot(prompt)

    # Process and display the chatbot_response as needed
    print(chatbot_response)

if __name__ == "__main__":
    main()
