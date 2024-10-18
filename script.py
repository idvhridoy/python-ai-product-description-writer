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

def generate_product_description(product_name, purchase_price, sale_price):
    prompt = f"""
    Write an SEO-ready, structured product description for a skincare product called "{product_name}". 
    The description should include:
    - An engaging title
    - A short description (1-2 sentences)
    - Bullet points for key features
    - An ingredients list (hypothetical)
    - Use cases for different skin types
    - Cautions (e.g., pregnancy, allergies)
    - Detailed information about the product's benefits
    - Common FAQs
    Purchase Price: ${purchase_price}
    Sale Price: ${sale_price}
    """
    
    # Make a request to the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant skilled in writing SEO-ready product descriptions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    # Extract the text from the API response
    description = response['choices'][0]['message']['content'].strip()
    return description

def main():
    # Load product data from the XLSX file
    products_df = pd.read_excel(input_file)
    
    # Prepare output data structure
    product_descriptions = []
    
    # Iterate over each product and generate descriptions
    for _, row in products_df.iterrows():
        product_name = row['product_name']
        purchase_price = row['purchase_price']
        sale_price = row['sale_price']
        
        # Generate the description
        description = generate_product_description(product_name, purchase_price, sale_price)
        
        # Store the result in a dictionary
        product_data = {
            "product_name": product_name,
            "purchase_price": purchase_price,
            "sale_price": sale_price,
            "description": description
        }
        
        # Add the product data to the list
        product_descriptions.append(product_data)
        
        # Print progress
        print(f"Generated description for {product_name}")
    
    # Save all descriptions to a JSON file
    with open(output_file, "w") as f:
        json.dump(product_descriptions, f, indent=4)
    
    print(f"All product descriptions saved to {output_file}")

if __name__ == "__main__":
    main()
