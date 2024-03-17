from pathlib import Path
import re

# add the items you want to parse from the receipt
labels = {
    'ks bath': 'toilet paper',
    'boomchickpop': 'boom chicka pop',
    'bananas': 'bananas',
    'ks 5dz eggs': 'eggs',
    'milk': 'milk',
    'watermelon': 'watermelon',
    'choc crepes': 'chocolate crepes',
    'greek pita': 'pita',
    'mini cookie': 'mini cookies',
    'bagels': 'bagels',
    'avocados ct': 'avocado',
    'org cucumber': 'cucumber',
    'shishito pep': 'shishito peppers',
    'lb org gala': 'gala apples',
    'lb org fuji': 'fuji apples',
    'strawberries': 'strawberries',
    'apple pear': 'apple pears',
    'green grapes': 'grapes',
    'frozen berry': 'frozen berries',
    'org broc lb': 'broccoli',
    'mandarins': 'mandarins',
    'pumpkin flax': 'granola',
    'smokd salmon': 'smoked salmon',
    'ks towel': 'paper towels',
    'org gre bean': 'green beans'
}

def parse_costco_receipt(file_path):
    parsed_data = {}
    unlabeled_data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print('open file')

            receipt_lines = file.readlines()
            print('raw data:\n', receipt_lines, '\n')
            
            for i in range(len(receipt_lines)):
                # clean the line, removing all spaces and special characters
                line = receipt_lines[i].strip().lower()
                cleaned_line = re.sub(r'[^A-Za-z\s]', '', line).strip().lower()
                item_found = False
                # check if line contains an item from the labels list
                for label in labels:
                    if label in cleaned_line:
                        item_found = True
                        # price should be in next line 
                        if i + 1 < len(receipt_lines):
                            price_line = receipt_lines[i + 1].strip()
                            # retrieve the price from the line
                            price_match = re.search(r'\d+\.\d+', price_line)
                            if price_match:
                                price = float(price_match.group())
                                # check if next line is a sale price 
                                # note: receipt format is a number sequence, then next line has the discount (2.00-)
                                if i + 4 < len(receipt_lines):
                                    sale_line = receipt_lines[i + 4].strip()
                                    sale_match = re.search(r'\d+\.\d+-', sale_line)
                                    # print(sale_line)
                                    # subtract the sale price from the price
                                    if sale_match:
                                        sale_price = float(sale_match.group()[:-1])
                                        price -= sale_price  
                                # add the item and price to the parsed data
                                parsed_data[labels[label]] = price
                                break
                if not item_found:
                    if i + 1 < len(receipt_lines):
                        price_line = receipt_lines[i + 1].strip()
                        # print(price_line)
                        price_match = re.search(r'\d+\.\d+', price_line)
                        if price_match:
                            price = float(price_match.group())
                            if i + 4 < len(receipt_lines):
                                sale_line = receipt_lines[i + 4].strip()
                                sale_match = re.search(r'\d+\.\d+-', sale_line)
                                # print(sale_line)
                                # subtract the sale price from the price
                                if sale_match:
                                    sale_price = float(sale_match.group()[:-1])
                                    price -= sale_price  
                        unlabeled_data[cleaned_line] = price
            return parsed_data, unlabeled_data
        
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return parsed_data

# receipt_file_path = r'data\test.txt'
receipt_file_path = Path('data') / 'test.txt'
parsed_data, unlabeled_data = parse_costco_receipt(receipt_file_path)
print('\nUnlabeled Items')
for item, price in unlabeled_data.items():
    print(f"{item}: ${price}")
print('\nLabeled Items')
for item, price in parsed_data.items():
    print(f"{item}: ${price}")


communals = []
user_input = input('Enter communals (separated by commas): ')
# while True:
#     user_input = input("Enter communals (type done to stop):")
    
#     # Check if the user wants to stop the input process
#     if user_input.lower() == 'done':
#         break
#     else:
#         # Append the input value to the list
#         communals.append(user_input)
communals = user_input.lower().split(', ')
total = 0       
for communal in communals:
    print(communal + ': $' + str(parsed_data[communal]))
    if communal in parsed_data:
        total += float(parsed_data[communal])
    else:
        total += float(unlabeled_data[communal])
print(f'Total: ${round(total, 2)}')
split = float(input('Enter number of people: '))
print(f'Each person owes: ${round(total / split, 2)}')