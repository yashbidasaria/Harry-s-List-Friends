import csv
from django.contrib.auth import get_user_model

UserModel = get_user_model()

#get the data from csv
with open('MOCK_DATA.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        user_name = str(row)
        print(user_name)
        pass_word = 'adeladel'
        if not UserModel.objects.filter(username=user_name).exists():
            user=UserModel.objects.create_user(user_name, password = pass_word)
            user.save()


