import yandex_geocoder

def enterparams():
    """
    Initialising global variables
    """
    global file_name, key, new_file_name, missing_file_name, limit
    key = input("Enter API Key: \n")
    file_name = input("Enter file name: \n")
    new_file_name = input("Enter Output File Name: \n")
    missing_file_name = new_file_name.split('.')[0] + ' missing.csv'
    limit = int(input("Enter request limit: \n"))



def connect_yandex():
    """"
    Connecting to Yandex API
    """

    global yan
    yan = yandex_geocoder.Client(key)


def read_address(adfile):
    """
    Read all addresses from file
    """

    global names
    readFile = open('input\\'+adfile, encoding='utf-16-le', mode='r')
    names = readFile.readlines()


def getcood(location):
    """
    Get coordinates from Yandex API and generate a line string to write to file
    """
    try:
        coordinates = yan.coordinates(location)
    except:
        print('Location not found')
        lng, lat = 0, 0
    else:
        lng, lat = coordinates
    linestring = location.rstrip() + "=" + str(lng) + "=" + str(lat) + "\n"
    print(linestring)
    return linestring


def write_to_file(line_list):
    """
    Write the location and co-ordiantes to file
    """
    writeFile = open('Output\\'+new_file_name, encoding='utf-16-le', mode='a')
    writeFile.write(line_list)
    writeFile.close()


def write_missing_to_file():
    """
    Write exceptions to a separate file
    """
    readFile = open('Output\\'+new_file_name, encoding='utf-16-le', mode='r')
    writeMissing = open('Output\\'+missing_file_name, encoding='utf-16-le', mode='a')
    r = readFile.readlines()
    for i in r:
        if '=0=0' in i:
            writeMissing.write(i)


def main():
    enterparams()
    connect_yandex()
    read_address(file_name)
    count = 0  # To limit the number of API Requests
    for i in names:  # Loop over locations and and write to file
        l = getcood(i)
        write_to_file(l)
        count += 1
        if int(count) >= limit:  # Exit loop on set limit
            break
    write_missing_to_file()  # Generate separate file for missing coordinates

    return 0


main()
