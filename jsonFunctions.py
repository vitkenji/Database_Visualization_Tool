import simplejson as json

def saveData(data, filePath):
    if not data:
        print("No data to write!")
        return
    try:
        with open(filePath, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, default=str)
            print(f"Data has been saved!")
    except Exception as e:
        print(f"An error occurred: {e}")

def readData(filePath):
    try:
        with open(filePath, 'r') as f:
            json_data = json.load(f)
        print(json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

    return json_data

def removeFile(filePath):
    with open(filePath, 'w') as f:
        pass

