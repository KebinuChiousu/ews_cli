import os

def get_config(config="config.ini"):
    # Create the config dir if it doesn't exist and return path to config.
    home = os.path.expanduser("~")
    folder = os.path.join(home,".owa")
    ensure_dir(folder)

    return os.path.join(folder,config)

def pause():
    # Wait for user input.
    programPause = input("Press the <ENTER> key to continue...")

def ensure_dir(path):
    # Create directory if it doesn't exist.
    if not os.path.exists(path):
        os.makedirs(path)

def get_entry(text,value):
    # Substitute {0} in text with value.
    return text.format(value)

def submenu_nav(values,prompt,idx,count,input_value=False, back=False):
    stop=len(values)-1
    np=0
    pp=0
    mm=0

    while True:
        print(prompt)
        print('')
        for i in range(0,len(values)):
            print(i, values[i])

        if idx < count:
            np=i+1
            i=i+1
            print(np, "Next Entry")
        if idx > 0:
            pp=i+1
            i=i+1
            print(pp, "Prev Entry")
        if back == True:
            if pp == 0:
                mm = np + 1
                print(mm, "Prev Menu")
            else:
                mm = pp + 1
                print(mm, "Prev Menu")
        print('')

        sel=int(input("Enter Selection: "))

        # Validate input is valid for current menu.
        if (sel >= 0) and (sel <= stop):
            if input_value:
                ret = sel
            else:
                ret = values[sel]
            break
        else:
            # Move 1 page ahead
            if sel == np:
                ret = "Next"
                break
            elif sel == pp:
                ret = "Prev"
                break
            elif sel == mm:
                ret = "Go Back"
                break
            else:
                print("Unknown Option Selected!")
                pause()
                _=os.system("clear")

    return ret

def submenu(values,prompt,input_value=False):
    inc=9
    start=0
    stop=inc
    np=0
    pp=0

    while True:
        print(prompt)
        print('')
        for i in range(start,len(values)):
            print(i, values[i])
            j=i
            # limit number of entries to stop var.
            if i >= stop:
                # Stop offering next if the last entry is reached.
                if i < (len(values)-1):
                    np=stop+1
                    i=i+1
                    print(np, "Next Page")
                    break
        #if stop > inc, allow prev page.
        if stop > inc:
            pp=i+1
            i=i+1
            print(pp, "Prev Page")
        print('')
        #parse input into number, blank is invalid.
        try:
            sel=int(input("Enter Selection: "))
        except:
            sel = j+1
        # Validate input is valid for current menu.
        if (sel >= start) and (sel <= j):
            if input_value:
                ret = sel
            else:
                ret = values[sel]
            break
        else:
            # Move 1 page ahead
            if sel == np:
                start=start+10
                stop=start+9
                _=os.system("clear")
            # Move 1 page back
            elif sel == pp:
                start=start-10
                stop=start+9
                _=os.system("clear")
            else:
                print("Unknown Option Selected!")
                pause()
                _=os.system("clear")

    return ret

def get_folder(folder, target):
    ret = None
    f = None
    f2 = ''

    if folder.absolute.replace('/root/Top of Information Store/Inbox/','') == target:
        return folder

    for f in folder.children:
        f2 = f.absolute.replace('/root/Top of Information Store/Inbox/','')
        if f2 in target:
            break

    if f2 == target:
        ret = f
    else:
        if f == None:
            return None
        else:
            ret = get_folder(f,target)

    return ret



