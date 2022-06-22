import requests
import functions
import jwt

endpoint = '159.65.32.17:2097'

def verify(token):
    try:
        return jwt.decode(token, "3B7B57346F526A3322DFD532AD9A6", algorithms=["HS256"])
    except Exception as error:
        return 0

def loadsession():
    return open('session.txt','r').read()

def savesession(token):
    open('session.txt','w').write(token)

def logout():
    open('session.txt','w').close()

def login(username,password):
    config = functions.loadconfig()
    data = {"username":username,"password":password}
    results = requests.post(f'http://{endpoint}/api/users/login', json = data)
    results = results.json()
    if (results['success'] == 1):
        verification = verify(results['message']['accesstoken'])
        if verification == 0:
            return 'Session expired - please relog'
        else:
            savesession(results['message']['accesstoken'])
            return 1
    else:
        return results['message']

def register(username,password):
    data = {"username":username,"password":password}
    results = requests.post(f'http://{endpoint}/api/users/registration', json = data)
    results = results.json()
    return results['message']

def listusers():
    results = requests.get(f'http://{endpoint}/api/users/listusers')
    results = results.json()
    return results

def deleteuser(username):
    data = {"username":username}
    results = requests.post(f'http://{endpoint}/api/users/deleteuser', json = data)
    results = results.json()
    return results['message']