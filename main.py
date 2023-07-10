import os, csv, requests, uuid, re


dir = input("Enter the file direction of the discord messages folder: ")

list_folder = [os.path.join(dir, folder)  for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]
if not os.path.isdir(dir + '/result'):
    os.mkdir(dir + '/result')

list_file = {}

def downloading_file_task():

    for e, f in list_file.items():
        print(str(list(list_file).index(e)) +  " / " + str(len(list(list_file))))

        if e.find('/'):
            file_name = e.rsplit('/', 1)[1]
        
        file_name = re.sub(r'[^\w_. -]', '_', file_name)
        
        if os.path.isfile(dir + '/result/' + file_name):
            file_name = str(uuid.uuid4()) + '_' + file_name

        if len(file_name) > 250:
            get_ext = os.path.splitext(file_name)
            file_name = str(uuid.uuid4()) + get_ext[-1] 
            

        r = requests.get(e, allow_redirects=True)
        open(dir + '/result/' + file_name, 'wb').write(r.content)

        # print(str(list(list_file).index(e)) +  " / " + str(len(list(list_file))), f, e)


def grab_file_from_csv_task(folder): 
    if os.path.isfile(folder + "\messages.csv"):
        with open(folder + "\messages.csv", 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            try:
                for row in reader:
                    column_value = row["Attachments"]
                    if column_value.startswith('https://cdn.discordapp.com'):
                        list_file[column_value] = folder + "\messages.csv"

            except ValueError:
                print('No Attachments column')


while True:        
    choice = input("Choose a specific concersation or export all (Specific: S | All : A) : ")

    if choice.lower() == 'a':
        for e in list_folder:
            grab_file_from_csv_task(e)
        downloading_file_task()
        break
    if choice.lower() == 's':
        i = 0
        for folder in list_folder:
            print(i, " - ", folder)
            i+=1
        while True:
            conv_choice = int(input("Enter the selected conversation number : "))
            if conv_choice >= 0 and conv_choice <= len(list_folder) - 1:
                grab_file_from_csv_task(list_folder[conv_choice])
                downloading_file_task()
                break
        break