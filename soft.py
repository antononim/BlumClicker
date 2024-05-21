import requests
import json

s = requests.Session()
accs = {}

def add_acc():
    name = input("Name: ")
    access = input("Access token: ")
    refresh = input("Refresh token: ")
    print("[i] Checking...")
    
    
    accs.update({name:(access,refresh)})
    save_accs()

def save_accs():
    # print(accs)
    with open("accs.json", "w+") as f:
        f.write(json.dumps(accs))
    print("[i] Accs dumped.")

def refresh_accs():
    global accs
    if ('Authorization' in s.headers): del s.headers['Authorization']
    for name in accs:
        # Check, if you need refreshing
        s.headers.update({"Authorization": "Bearer "+accs[name][0]})
        res = s.get("https://gateway.blum.codes/v1/user/me")
        # print(res)
        # print(res.content)
        
        if (res.status_code != 200):
            # Then refresh token.
            res = s.post('https://gateway.blum.codes/v1/auth/refresh', data='{"refresh":"'+accs[name][1]+'"}')
            tokens = json.loads(res.content)
            # Check if succeed at getting new token
            if (not ('access' in tokens)): 
                print(f"[e] Invalid token at \'{name}\' ")
                if ('message' in tokens): print(f"[e] Message from server: {tokens['message']}")
                continue
            accs[name][0] = tokens['access']
            accs[name][1] = tokens['refresh']
            print(f"[i] Refreshed token for '{name}'!")
            # print(accs[name])
        else:
            print(f"[i] No refresh needed for {name}!")
    save_accs()

def claim_accs():
    for name in accs:
        s.headers.update({"Authorization": "Bearer "+accs[name][0]})
        while(True):
            try:
                res = s.post("https://game-domain.blum.codes/api/v1/farming/claim")
                res = s.post("https://game-domain.blum.codes/api/v1/farming/start")
                print(f"[i] Claimed for '{name}'")
                break;
            except:
                continue;

def main():
    global accs
    with open("accs.json", "r") as f:
        inners = f.read()
    if (inners == "" or not json.loads(inners)):
        print("[e] File is kinda empty")
        accs = {"example": ("access", "refresh")}
        save_accs()
    else:
        accs = json.loads(inners)

    # print(accs)
    
    # Prepare session
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"})
    s.headers.update({"DNT":"1"})
    s.headers.update({"Accept":"application/json, text/plain, */*"})
    # s.headers.update({"Authorization": "Bearer "+token})
    
    refresh_accs()
    claim_accs()
    


if __name__ == "__main__":
    main()