import smtplib, ssl
from random import shuffle
from random import choice
port = 465  # For SSL
smtp_server = "smtp.gmail.com"

# Function that will create a match for every player
def getSecretSantas(names):
    matches = {}
    for i in range(len(names)):
        # Flag variable
        namesMatch = True
        while namesMatch:
            namesMatch = False
            selection = choice(names)
            # If the person selected themselves then redo
            if (selection == names[i]):
                namesMatch = True
            else:
                # If they selected someone that had already been chosen redo
                if selection in matches.values():
                        namesMatch = True
        matches[names[i]] = selection
    return matches

# Getting Users Input
while(True):
    senderEmail = input("What is your email address? ")
    # Using a gmail server so we have to make sure the sender is a gmail account
    if (('@gmail.com') == senderEmail[-10:]):
        break
    else:
        print("Please enter an email ending in '@gmail.com'")
        print()
password = input("What is your password? ")
while (True):
    limitAmount = input("What is the limit amount? ")
    if not(int(limitAmount) < 0):
        break
    else:
        print("Please enter a positive amount")
        print()
while (True):
    print('Would you like to allow people to get eachother?')
    samePerson = input("For yes type just 'Y' and for no type and press enter on 'N': ")
    if ((samePerson == 'Y') or (samePerson == 'N')):
        break
    else:
        print("Please enter either a 'Y' or a 'N'")
        print()

while(True):
    print("What are the names and emails of the participants (email should follow the name seperated by a space)? ")
    names = input('Ex. John johndoe@gmail.com Eve eve123@gmail.com etc...: ')
    names = names.split(' ')
    recieverEmail = ""
    tempEmail = ''
    emails = []
    matchedEmails = {}
    chosen = {}
    # Get the emails in a seperate list from the names
    for i in range(int(len(names) / 2)):
        tempEmail = names.pop(i + 1)
        matchedEmails[tempEmail] = names[i]
        emails.append(tempEmail)
    # If they didn't give enough people to have different secret santas
    if not(len(names) < 3 and samePerson == 'Y'):
        break
    else:
        print("You must have more than 2 people so they can't get eachother")
        print()

# Shuffle to add to the randomness a little
shuffle(names)

# If it's okay for players to get eachother then we can just call the function regularly
if samePerson:
    chosen = getSecretSantas(names)
else:
    # Flag variable
    notOptimal = True
    while notOptimal:
        notOptimal = False
        chosen = getSecretSantas(names)
        for person in names:
            # If the two people have eachother then we need to redo.
             if person == chosen[chosen[person]]:
                 notOptimal = True

message = """\
Subject: Hi {}

You are a secret santa to {}.
Gifts should be under ${}!
- Secret Santa Matcher"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(senderEmail, password)
    for recieverEmail in emails:
        # print(recieverEmail, message.format(matchedEmails[recieverEmail], chosen[matchedEmails[recieverEmail]]), limitAmount)
        server.sendmail(senderEmail, recieverEmail, message.format(matchedEmails[recieverEmail], chosen[matchedEmails[recieverEmail]], limitAmount))

print('Done sending emails')