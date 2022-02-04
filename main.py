import subprocess
import json


def save_data(name, passw):
    """ Save data to JSON file """
    with open('passwords.json', 'a') as f_obj:
        user_data = [
            {
                'WiFi Name': name,
                'Password': passw
            }
        ]
        json.dump(user_data, f_obj, sort_keys=False, indent=4)  


def profile_list():
    """ Get a list of all wlan profiles """
    all_profiles = subprocess.run('netsh wlan show profiles', stdout=subprocess.PIPE,
                                  encoding='utf-8')
    profiles = [i.split(':')[1].strip() for i in all_profiles.stdout.split('\n')
                if 'All User Profile' in i]
    return profiles
    
    
def get_password(profiles):
    """ Get a password for each profile """    
    for profile in profiles: 
        password_raw = subprocess.run(f'netsh wlan show profile "{profile}" key=clear',
                                      stdout=subprocess.PIPE, encoding='utf-8')
        password = [i.split(':')[1].strip() for i in password_raw.stdout.split('\n') 
                    if 'Key Content' in i][0]
        save_data(profile, password)


def main():
    """ Run a script """
    try:
        get_password(profile_list())
    except IndexError:
        pass
    

if __name__ == '__main__':
    main()
    
