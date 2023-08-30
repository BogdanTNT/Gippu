import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Use a service account.
cred = credentials.Certificate('whoinlab-firebase-adminsdk-m8phl-0a882e298f.json')

fbapp = firebase_admin.initialize_app(cred)

db = firestore.client()

def IsHeOnDatabase(localIp) -> bool:
    user_ref = db.collection(u'PeopleInLab')
    docs = user_ref.stream()

    # print(docs)

    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()}')
        if localIp == doc.to_dict()["ip"]:
            return True
    
    return False

def UploadEvent(name, date, ip = None):
    user_ref = db.collection(f'PeopleInLab/{name}/{date.year}/{date.month}/{date.day}')
    docs = user_ref.stream()
    
    count = 0
    for doc in docs:
        count = count + 1

    doc_ref = db.collection(f'PeopleInLab/{name}/{date.year}/{date.month}/{date.day}').document(f"Event{count}")
    doc_ref.set({
        u'hour': date.time().hour,
        u'minute': date.time().minute,
        u'second': date.time().second
    })

    if ip is not None:
        doc_ref = db.collection(f'PeopleInLab').document(name)
        doc_ref.set({
            u'name': name,
            u'ip': ip
        })

def GetPersonel():
    user_ref = db.collection(u'PeopleInLab')
    docs = user_ref.stream()

    personel = []

    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()}')
        personel.append(doc.to_dict())

    return personel

def GetEveryoneInLab(today):
    personel = GetPersonel()

    peopleInLab = []

    for person in personel:
        user_ref = db.collection(f'PeopleInLab/{person["name"]}/{today.year}/{today.month}/{today.day}')
        docs = user_ref.stream()
        
        count = 0
        for doc in docs:
            count = count + 1

        if count % 2 == 1 and count > 0:
            peopleInLab.append(person['name'])
    return peopleInLab
