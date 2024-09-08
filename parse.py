from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3.1")

# static test to make sure model is working
def parse_with_ollama_test():
    # Simple test input for the model
    dom_content = "This is a simple test string."
    parse_description = "Extract the word 'test'."
    
    # Combine dom_content and parse_description into a single string
    formatted_prompt = f"Content: {dom_content}\nInstructions: {parse_description}"
    
    # Print the formatted prompt for debugging
    print(f"Formatted Prompt:\n{formatted_prompt}")

    try:
        # Invoke the model with a string input
        response = model.invoke(formatted_prompt)  # Pass the formatted string, not a dictionary
        print(f"Direct response: {response}")
        return response
    except Exception as e:
        print(f"Error invoking model: {e}")
        return str(e)


def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)