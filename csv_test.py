import csv

i=0

while True:
    while(i==0):
        with open('rest.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for col in reader:
                print(col[0])
                i+=1
        csvfile.close()





