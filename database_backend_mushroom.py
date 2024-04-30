import requests
import json
import hashlib

def fetch_attributes(url):
    """
    Fetch attribute mappings from Firebase.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data")

#firebase db containing the mapping data
firebase_url = "https://dsci551-project-af6fd-default-rtdb.firebaseio.com/.json"

#load keys/attributes (of the target and feature variables) from Firebase
attributes = fetch_attributes(firebase_url)['key']

DATABASE_URLS = {
    0: "https://dsci551-project-af6fd-db0.firebaseio.com/",
    1: "https://dsci551-project-af6fd-db1.firebaseio.com/",
    2: "https://dsci551-project-af6fd-db2.firebaseio.com/",
    3: "https://dsci551-project-af6fd-db3.firebaseio.com/",
    4: "https://dsci551-project-af6fd-db4.firebaseio.com/",
    5: "https://dsci551-project-af6fd-db5.firebaseio.com/",
    6: "https://dsci551-project-af6fd-db6.firebaseio.com/",
    7: "https://dsci551-project-af6fd-db7.firebaseio.com/",
}

def gen_hash(gillcolor, capcolor, habitat):
    new_string = f"{gillcolor}{capcolor}{habitat}"
    hash_obj = hashlib.sha256(new_string.encode())
    hash_num = int(hash_obj.hexdigest(), 16)
    return hash_num % len(DATABASE_URLS)

def prompt_for_input(attribute):
    """
    prrompt user for input, showing valid options
    """
    options = attributes[attribute]
    print(f"Enter {attribute} ({', '.join([f'{k}: {v}' for k, v in options.items()])}): ")
    while True:
        user_input = input().strip()
        if user_input in options.values():
            return user_input
        print("Invalid input, please try again.")

def get_next_index():
    """
    finds the highest index from all databases and returns the next available index
    """
    max_index = 8123  #start from this if no higher index found
    for db_id, url in DATABASE_URLS.items():
        response = requests.get(f"{url}.json?shallow=true")
        if response.status_code == 200:
            data = response.json()
            if data:
                max_index = max(max_index, max(map(int, data.keys())))
    return max_index + 1

def add_data():
    """
    adds new data to the appropriate database with incremental index
    """
    data = {attr: prompt_for_input(attr) for attr in attributes}
    db_id = gen_hash(data['gill-color'], data['cap-color'], data['habitat'])
    next_index = get_next_index()
    
    url = f"{DATABASE_URLS[db_id]}/{next_index}.json"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print(f"Data added to DB {db_id}, index: {next_index}")
    else:
        print("Failed to add data, status code:", response.status_code)


def update_data():
    """
    updates inputted atribute value for inputted index
    gen_hash used as necessary to update db location for given index (transfers data to new db and then removes data from old db)
    """
    index = input("Enter the index of the data to update: ")
    attribute = input("Enter the attribute to update: ")
    value = prompt_for_input(attribute)

    found = False
    for db_id, url in DATABASE_URLS.items():
        response = requests.get(f"{url}/{index}.json")
        if response.status_code == 200 and response.json() is not None:
            existing_data = response.json()
            original_db_id = db_id
            found = True
            break

    if not found:
        print("Data not found in any database.")
        return

    #set the inputted value for inputted attribute
    existing_data[attribute] = value

    #determine if updated attribute affects db hash
    hash_affected = attribute in ['gill-color', 'cap-color', 'habitat']
    new_db_id = gen_hash(existing_data['gill-color'], existing_data['cap-color'], existing_data['habitat']) if hash_affected else original_db_id

    if new_db_id != original_db_id and hash_affected:
        move_response = requests.put(f"{DATABASE_URLS[new_db_id]}/{index}.json", json=existing_data)
        if move_response.status_code == 200:
            #deletes original data if succesfully moved to new db
            delete_response = requests.delete(f"{DATABASE_URLS[original_db_id]}/{index}.json")
            if delete_response.status_code == 200:
                print(f"Data moved and updated to DB {new_db_id} from DB {original_db_id}, maintained index: {index}")
            else:
                print(f"Failed to delete original data from DB {original_db_id}, status code: {delete_response.status_code}")
        else:
            print(f"Failed to update data in new DB {new_db_id}, status code: {move_response.status_code}")
    else:
        #update in existing bc hash not affected
        update_response = requests.put(f"{DATABASE_URLS[original_db_id]}/{index}.json", json=existing_data)
        if update_response.status_code == 200:
            print(f"Data updated in original DB {original_db_id}, at index: {index}")
        else:
            print(f"Failed to update data, status code: {update_response.status_code}")


def delete_data():
    """
    delete entire index (data) from a specific database
    asks for 2 inputs (db ID and index) to make sure user is certain about deleting data at inputted index
    """
    db_id = int(input("Enter the database ID: "))
    index = input("Enter the index of the data to delete: ")
    url = f"{DATABASE_URLS[db_id]}/{index}.json"
    
    response = requests.get(url)
    if response.status_code == 200 and response.json() is not None:
        #data exists, proceed to delete
        del_response = requests.delete(url)
        if del_response.status_code == 200:
            print("Data successfully deleted.")
        else:
            print("Failed to delete data, status code:", del_response.status_code)
    else:
        print("Data not found at the specified index, nothing to delete.")

def read_data():
    """
    reads all data at inputted index
    """
    index = input("Enter the index of the data to retrieve: ")
    data_found = False
    for db_id, url in DATABASE_URLS.items():
        response = requests.get(f"{url}/{index}.json")
        if response.status_code == 200 and response.json() is not None:
            data = response.json()
            print(f"Data found in DB {db_id}:", json.dumps(data, indent=4))
            data_found = True
            break

    if not data_found:
        print("Data not found in databases at the specified index.")

def main():
    while True:
        print("1. Add Data")
        print("2. Read Data")
        print("3. Update Data")
        print("4. Delete Data")
        print("5. Exit")           
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_data()
        elif choice == '2':
            read_data()
        elif choice == '3':
            update_data()
        elif choice == '4':
            delete_data()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

