# analyze the wellness score for one user

import json

def user_wellness(screen_name):
    # should return a dictionary that gives a wellness score for each week
    # and each month that the user was active.
    pass

if __name__ == '__main__':
    # pass in the username of the account you want to download
    data = user_wellness("jayhersk")

    # write the json file
    with open(screen_name + '_wellness.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

