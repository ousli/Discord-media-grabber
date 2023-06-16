import os, csv, requests, uuid

dir = input("Enter the file direction of the discord messages folder: ")

list_folder = [os.path.join(dir, folder)  for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]
if not os.path.isdir(dir + '/result'):
    os.mkdir(dir + '/result')
for folder in list_folder:
    if os.path.isfile(folder + "\messages.csv"):
        
        with open(folder + "\messages.csv", 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
        
                # Get the value in the target column for the current row
            try:
                for row in reader:
                    # Check if the value starts with the desired condition
                    column_value = row["Attachments"]
                    if column_value.startswith('https://cdn.discordapp.com'):

                        if column_value.find('/'):
                            file_name = column_value.rsplit('/', 1)[1]

                        if os.path.isfile(dir + '/result/' + file_name):
                            file_name = str(uuid.uuid4()) + '_' + file_name

                        r = requests.get(column_value, allow_redirects=True)
                        open(dir + '/result/' + file_name, 'wb').write(r.content)
                        print(column_value)
            except ValueError:
                print('No Attachments column')