import csv
import random
import os

# Function to generate random data for input_product.csv
def generate_input_product(num_records):
    products = []
    for i in range(1, num_records + 1):
        product_id = i
        product_hashtags = [f'hashtag{random.randint(1, 99)}' for _ in range(2)]
        products.append([product_id, ','.join(product_hashtags)])
    return products

# Function to generate random data for input_customer.csv
def generate_input_customer(num_records, num_products):
    customers = []
    for i in range(101, 101 + num_records):
        customer_id = i
        product_id = random.randint(1, num_products)
        customers.append([customer_id, product_id])
    return customers

# Function to generate random data for input_price.csv
def generate_input_price(num_products):
    prices = []
    for i in range(1, num_products + 1):
        product_id = i
        price = round(random.uniform(100, 1000), 2)
        prices.append([product_id, price])
    return prices

# Function to generate random data for input_newhashtags.csv
def generate_input_newhashtags(num_records, num_products):
    new_hashtags = []
    for i in range(num_records):
        product_id = random.randint(1, num_products)
        product_hashtags = [f'hashtag{random.randint(1, 99)}' for _ in range(random.randint(1, 3))]
        new_hashtags.append([product_id, ','.join(product_hashtags)])
    return new_hashtags

# Function to write data to CSV file
def write_to_csv(filename, data, headers):
    os.makedirs('./SameSizeTests', exist_ok=True)
    filepath = os.path.join('./SameSizeTests', filename)
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Main function to generate test cases
def generate_test_cases(num_test_cases, num_records, num_products, num_new_hashtags_rows):
    for i in range(1, num_test_cases + 1):
        write_to_csv(f'{i}_input_product.csv', generate_input_product(num_products), ['product_id', 'hashtags'])
        write_to_csv(f'{i}_input_customer.csv', generate_input_customer(num_records, num_products), ['customer_id', 'product_id'])
        write_to_csv(f'{i}_input_price.csv', generate_input_price(num_products), ['product_id', 'price'])
        write_to_csv(f'{i}_input_newhashtags.csv', generate_input_newhashtags(num_new_hashtags_rows, num_products), ['product_id', 'hashtags'])

def generate_test_cases_increasing_size(parameter : str):
    # This function generates test cases with increasing size based on the parameter
    # The parameter can be 'num_records' or 'num_products' or 'num_new_hashtags_rows'
    for i in range(1, num_test_cases + 1):
        if parameter == 'num_records':
            num_records = i * 10000  # Increase number of records
            num_products = 10000  # Keep products constant
            num_new_hashtags_rows = 10  # Keep new hashtags constant
        elif parameter == 'num_products':
            num_records = 10000  # Keep records constant
            num_products = i *10000  # Increase number of products
            num_new_hashtags_rows = 10  # Keep new hashtags constant
        elif parameter == 'num_new_hashtags_rows':
            num_records = 10000  # Keep records constant
            num_products = 10000  # Keep products constant
            num_new_hashtags_rows = 5*i  # Increase number of new hashtags rows
        else:
            raise ValueError("Invalid parameter. Choose from 'num_records', 'num_products', or 'num_new_hashtags_rows'.")

        write_to_csv(f'{i}_input_product.csv', generate_input_product(num_products), ['product_id', 'hashtags'])
        write_to_csv(f'{i}_input_customer.csv', generate_input_customer(num_records, num_products), ['customer_id', 'product_id'])
        write_to_csv(f'{i}_input_price.csv', generate_input_price(num_products), ['product_id', 'price'])
        write_to_csv(f'{i}_input_newhashtags.csv', generate_input_newhashtags(num_new_hashtags_rows, num_products), ['product_id', 'hashtags'])

# Example usage
if __name__ == "__main__":
    num_test_cases = 30
    num_records = 100000  # Number of records in input_customer.csv
    num_products = 100000  # Number of products in input_product.csv and input_price.csv
    num_new_hashtags_rows = 10  # Number of rows in input_newhashtags.csv
    # generate_test_cases(num_test_cases, num_records, num_products, num_new_hashtags_rows)
    generate_test_cases_increasing_size('num_records')
