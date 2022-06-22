import datetime
import re
import string
import random
import base64



def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

def translator(message, email):
    encrypt = attachment = False
    commands = re.findall('\{\{(.*?)\}\}',message)
    emailname = email.split('@')[0]
    domain = email.split('@')[1]

    for command in commands:
        translated = f'{{{{{command}}}}}'
        if 'date-' in command:
            date = datetime.datetime.now()
            command =  date.strftime(command.split('date-')[1])
            message = message.replace(translated, command)
        elif 'random-n-' in command:
            command = random_with_N_digits(int(command.split('random-n-')[1]))
            message = message.replace(translated, str(command))
        elif 'random-s-' in command:
            command = command.split('random-s-')[1]
            message = message.replace(translated, ''.join(random.choice(string.ascii_uppercase) for _ in range(int(command))))
        elif 'encrypt' in command:
            encrypt = True
            message = message.replace(translated,'')
        elif 'attachment' in command:
            attachment = re.findall('\[(.*?)\]',command.split('attachment')[1])[0].split(',')
            message = message.replace(translated,'')
        else:
            message = message.replace(translated, locals()[command])

        if encrypt:
            string_bytes = message.encode("ascii")
            message = str(base64.b64encode(string_bytes))

    return(message, attachment)