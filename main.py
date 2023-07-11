import os, csv, requests, uuid, re


dir = input("Enter the file direction of the discord messages folder: ")

list_folder = [os.path.join(dir, folder)  for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]




def downloading_file_task(export_dir, file_list):
    
    for e, f in file_list.items():
        print(str(list(file_list).index(e)) +  " / " + str(len(list(file_list))))
        
        if e.find('/'):
            file_name = e.rsplit('/', 1)[1]
        
        file_name = re.sub(r'[^\w_. -]', '_', file_name)
        dir = export_dir
        if export_dir == None:
            dir = str(f).replace('\\messages.csv', '')
            dir = dir.replace('\\\\', '\\')
        if not os.path.isdir(dir + '/result'):
            os.mkdir(dir + '/result')
        if os.path.isfile(dir + '/result/' + file_name):
            file_name = str(uuid.uuid4()) + '_' + file_name

        if len(file_name) > 250:
            get_ext = os.path.splitext(file_name)
            file_name = str(uuid.uuid4()) + get_ext[-1] 
            

        r = requests.get(e, allow_redirects=True)
        open(dir + '/result/' + file_name, 'wb').write(r.content)


def grab_file_from_csv_task(folder, listefile):
    if os.path.isfile(folder + "\messages.csv"):
        with open(folder + "\messages.csv", 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            try:
                for row in reader:
                    column_value = row["Attachments"]
                    if column_value.startswith('https://cdn.discordapp.com'):
                        listefile[column_value] = folder + "\messages.csv"
            except ValueError:
                print('No Attachments column')
    return listefile


while True:   
    choice = input("Choose a specific concersation or export all (Specific: S | All : A) : ")

    if choice.lower() == 'a':

        list_file = {}
        print('Export Options :')
        print("1 - Export all media in a single folder")
        print("2 - Separate according to conversations")
        output_choix = int(input("1 or 2 : "))
        while True:
            if output_choix == 1:
                for e in list_folder:
                    list_file = grab_file_from_csv_task(e, list_file)
                downloading_file_task(dir, list_file)
                print("Files downloaded successfully !")
                print(f'Export dir : dir\\result')
                break
            if output_choix == 2:
                for e in list_folder:
                    list_file = grab_file_from_csv_task(e, list_file)
                downloading_file_task(None, list_file)
                print("Files downloaded successfully !")
                print('You will be able to find the result file in each associated conversariob folder')
                break
            
       
        break
    if choice.lower() == 's':
        i = 0
        for folder in list_folder:
            print(i, " - ", folder)
            i+=1
        while True:
            list_file = {}
            conv_choice = int(input("Enter the selected conversation number : "))
            if conv_choice >= 0 and conv_choice <= len(list_folder) - 1:
                print(list_folder[conv_choice])
                list_file = grab_file_from_csv_task(list_folder[conv_choice], list_file)
                downloading_file_task(list_folder[conv_choice], list_file)
                print("Files downloaded successfully !")
                print(f'Export dir : {list_folder[conv_choice]}\\result')
                break
        break