import json, os, csv, traceback

fileList = os.listdir(f"{os.getcwd()}/output")

clans = {
    "clans": [
        {"name": "Rob-Seb", "tag": "#8Q0L9CRY"},
        {"name": "Vi11ageWarriors", "tag": "#LL2C8L8V"},
        {"name": "Invidia Bandit", "tag": "#9VG8P90Q"},
        {"name": "#THE SHIELD#", "tag": "#PGPPQRLY"},
        {"name": "Immortal Rising", "tag": "#28Q99QL0Q"},
        {"name": "Spartan Warrior", "tag": "#20LGGU0R"},
        {"name": "Indian Prestige", "tag": "#PQJUJCPL"},
        {"name": "No Mercy", "tag": "#LLJCVJQL"},
        {"name": "Petiks Lang", "tag": "#9UVC0RV0"}
    ]
}

def dataCollect(file, clanName):
    with open(f"{os.getcwd()}/output/{file}", "r") as f:
        data = json.load(f)
        return [member for member in data['clans'][clanName]]
    
def csvSave(file, data):
    count = 0
    try:
        with open(f"{os.getcwd()}/csv/{file}.csv", mode='w', newline='') as f:
            write = csv.writer(f)
            for entry in data:
                if count == 0:
                    write.writerow(entry.keys())
                    count += 1
                else:
                    write.writerow(entry.values())
            
            return True
    except Exception:
        print(traceback.format_exc())
        return False

def main():
    dataReady = []
    for file in fileList:
        print(f"opening {file}")
        for clan in clans['clans']:
            try:
                dataList = dataCollect(file, clan['name'])
                for data in dataList:
                    data["name"] = data["name"].encode('ascii', 'ignore').decode('ascii')
                    data['clanName'] = clan['name']
                    data['clanTag'] = clan['tag']
                    dataReady.append(data)
            except Exception as e:
                print(traceback.format_exc())
                pass
        
    csvSave("test",dataReady)

print(main())