import os
import openai
import pandas as pd
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# File paths
input_file = "data/products.xlsx"
output_file = "output/product_descriptions.json"

# Role prompt and primer
role_prompt = """
    Assume the role of an expert content and product description writer with years of experience and a proven track record.
    You have written millions of SEO-ready product descriptions that are engaging, informative, and adhere to professional content-writing standards.
    You possess excellent grammar skills and are skilled at writing content that resonates with readers, encouraging engagement.
    Additionally, you have expertise in following all the best practices of content writing, ensuring each description is comprehensive, powerful, and relatable.
"""

primer = """
    Your task is to write SEO-ready, structured product descriptions for skincare products. Each description should include the following structure:
    - Title (engaging, with a focus keyword)
    - Short description (1-2 sentences)
    - Bullet points for key features
    - Ingredients list (hypothetical)
    - Skin Types
    - Use cases for different skin types
    - Cautions (e.g., pregnancy, allergies)
    - Detailed (6-8 sentences) information about the product's benefits
    - Common FAQs with answers with Q for question and A for answer
    - Write a heart tempting hooks
    - Meta Title
    - Meta Description
    Ensure each section is clearly labeled and the description is comprehensive, formatted clearly, and written in a professional tone.
"""

def send_primer():
    """
    Sends the initial primer message to OpenAI API to establish context.
    """
    openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": primer}
        ],
        max_tokens=150,
    )
    print("Primer set successfully.")

def generate_product_description(product_name):
    """
    Generates a product description based on the product name.
    """
    prompt = f"""
    Write an SEO-ready, structured product description for the skincare product called '{product_name}'. 
    Please follow this structure:
    - Title: 
    - Short Description: 
    - Key Features: 
    - Ingredients: 
    - Skin Types:
    - Use Cases: 
    - Cautions: 
    - Detailed Benefits: 
    - Common FAQs:
    - Hooks: 
    - Meta Title: 
    - Meta Description: 
    Make sure to search the internet for authentic and valuable content before writing.
    """

    # Make a request to the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.7
    )
    
    # Extract the text from the API response
    description = response['choices'][0]['message']['content'].strip()
    return description

def main():
    # Send the primer message to the API
    send_primer()
    
    # Load product data from the XLSX file
    products_df = pd.read_excel(input_file)
    
    # Prepare output data structure
    product_descriptions = []
    
    # Iterate over each product and generate descriptions
    for _, row in products_df.iterrows():
        product_name = row['product_name']
        
        try:
            # Generate the description
            description = generate_product_description(product_name)
            
            # Store the result in a dictionary
            product_data = {
                "product_name": product_name,
                "description": description
            }
            
            # Add the product data to the list
            product_descriptions.append(product_data)
            
            # Print progress
            print(f"Generated description for {product_name}")
        
        except Exception as e:
            print(f"Failed to generate description for {product_name}: {e}")
    
    # Save all descriptions to a JSON file
    with open(output_file, "w") as f:
        json.dump(product_descriptions, f, indent=4)
    
    print(f"All product descriptions saved to {output_file}")

if __name__ == "__main__":
    main()
