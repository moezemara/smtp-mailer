email list => add your email list to list.txt each email in one line

<-------------->

You have two files to add commands => template.txt and template.html
you can edit both with your custom commands and both will be sent

commands allowed:

###you have to put these commands in two brackets like this {{here}}

# emailname
the left part of the email
ex: example@gmail.com => example

# domain
the left part of the email
ex: example@gmail.com => gmail.com

# date-
date format: you write the format you want after the -
check table in for acceptable formats: https://www.w3schools.com/python/python_datetime.asp
ex: date-%d/%m/%Y => 28/8/2021

# random-s-
random string
you have to put the number of requested strings after the -
ex: random-s-3 => AGS

# random-n-
random numbers
you have to put the number digits after the -
ex: random-n-5 => 18639

# encrypt
BASE64 encrypt the message

# attachment[]
write the names of attachments to be sent seperated by a comma in the two brackets
ex: attachment[report.xls,new.doc]
ps: files should be added to the files folder


<--------------->
Configuration => config.txt
Config is a dictionary you can edit its values
username => your smtp username
password => your smtp password
smtp => smtp host
port => smtp port
from => What to write in email from
subject => emails subject