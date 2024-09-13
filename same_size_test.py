import os
import random
import csv
import subprocess
import argparse

# Directory containing the generated test case files
input_dir = "A1/Q1_profiling"
# Output file to store the results
output_file = "A1/Q1_profiling/output_results.txt"
# Path to the main executable
main_executable = "./A1/main"  # Change this to the path of your main executable

# Create the output directory if it doesn't exist
os.makedirs(input_dir, exist_ok=True)

# Function to generate random float numbers
def generate_random_float(min_value, max_value):
    return round(random.uniform(min_value, max_value), 2)

# Function to generate random integer numbers
def generate_random_int(min_value, max_value):
    return random.randint(min_value, max_value)

# Function to generate i_input_product.csv
def generate_products_file(file_path, num_products, num_hashtags):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["product_id", "hashtags"])  # Column names
        for product_id in range(1, num_products + 1):
            hashtags = [f"hashtag{generate_random_int(1, 100)}" for _ in range(num_hashtags)]
            writer.writerow([product_id] + hashtags)

# Function to generate i_input_customer.csv
def generate_customers_file(file_path, num_customers, num_products):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["customer_id", "product_id"])  # Column names
        for customer_id in range(1, num_customers + 1):
            num_purchases = generate_random_int(1, 10)
            purchases = [generate_random_int(1, num_products) for _ in range(num_purchases)]
            for product_id in purchases:
                writer.writerow([customer_id, product_id])

# Function to generate i_input_price.csv
def generate_prices_file(file_path, num_products):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["product_id", "price"])  # Column names
        for product_id in range(1, num_products + 1):
            price = generate_random_float(1.0, 1000.0)
            writer.writerow([product_id, price])

def generate_test_cases(num_cases, num_products, num_customers, num_hashtags):
    for i in range(1, num_cases + 1):
        products_file_path = os.path.join(input_dir, f"{i}_input_product.csv")
        customers_file_path = os.path.join(input_dir, f"{i}_input_customer.csv")
        prices_file_path = os.path.join(input_dir, f"{i}_input_price.csv")

        generate_products_file(products_file_path, num_products, num_hashtags)
        generate_customers_file(customers_file_path, num_customers, num_products)
        generate_prices_file(prices_file_path, num_products)

        print(f"Test case {i} files generated successfully in {input_dir}.")

def run_test_case(test_case_number):
    # Construct the file paths for the current test case
    product_file = os.path.join(input_dir, f"{test_case_number}_input_product.csv")
    customer_file = os.path.join(input_dir, f"{test_case_number}_input_customer.csv")
    price_file = os.path.join(input_dir, f"{test_case_number}_input_price.csv")

    # Additional arguments (replace these with actual arguments as needed)
    groups_path = os.path.join(input_dir, f"group_path")
    outputPath = os.path.join(input_dir, f"outputPath") 
    outputPath2 = os.path.join(input_dir, f"outputPath2")
    outputPath3 = os.path.join(input_dir, f"outputPath3")
    newHashtagPath = os.path.join(input_dir, f"newHashtagPath")

    # Command to run the main program with the input files and additional arguments
    command = [
        main_executable, 
        product_file, 
        customer_file, 
        price_file, 
        groups_path, 
        outputPath, 
        outputPath2, 
        outputPath3, 
        newHashtagPath
    ]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Append the output to the output file
    with open(output_file, "a") as f:
        f.write(f"Input {test_case_number}\n")
        f.write(result.stdout)
        f.write("\n--\n--\n")

def main():

    parser = argparse.ArgumentParser(description="Generate and run test cases.")
    parser.add_argument("-N", type=int, default=10, help="Number of test cases")
    parser.add_argument("-p", type=int, default=10000, help="Number of products")
    parser.add_argument("-c", type=int, default=10000, help="Number of customers")
    parser.add_argument("-t", type=int, default=5, help="Number of hashtags per product")
    
    args = parser.parse_args()

    # Number of test cases
    N = args.N
    # Number of products
    num_products = args.p
    # Number of customers
    num_customers = args.c
    # Number of hashtags per product
    num_hashtags = args.t

    # Generate test cases
    generate_test_cases(N, num_products, num_customers, num_hashtags)

    # Clear the output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run each test case and collect the outputs
    for i in range(1, N + 1):
        run_test_case(i)

    print(f"Outputs collected successfully in {output_file}.")

if __name__ == "__main__":
    main()