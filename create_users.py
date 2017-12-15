import csv
from django.contrib.auth import get_user_model

UserModel = get_user_model()

#get the data from csv
with open('MOCK_DATA.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        print(row)
        pass_word = 'adeladel'
        if not UserModel.objects.filter(username=row).exists():
            user=UserModel.objects.create_user(row, password = pass_word)
            user.save()


