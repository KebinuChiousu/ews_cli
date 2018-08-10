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
