#Runs on 1280 x 720 screen resolution

#space to quit
#ctrl-p to pause
#ctrl-b for bosskey
#semicolon to cheat

#all images have been created by the developer or have been taken from opengameart.org

from tkinter import *
from random import randint
import datetime
import os

def progstart():
    window.update_idletasks()
    window.bind("<space>", lambda event: event.widget.quit())
    score_label()
    entername()

def score_label():
    global score
    score=Label(canvas, font="Helvetica 16", width=20, background="blue", text="100")
    score.pack(anchor="n")

def entername():
    usrname_frame= LabelFrame(window, fg="white", bg="orange", text="Username")
    usrname_frame.place(x=0, y=0, width=w, height=h)

    evilcar=Label(usrname_frame, image=evilcar_img)
    evilcar.pack()
    usrname_label=Label(usrname_frame, fg="white", bg="black", text="Enter Username")
    usrname_label.pack(padx=5, pady=5)

    enter_usr=Entry(usrname_frame, bd=5)
    enter_usr.pack(padx=5, pady=5)

    submit_button=Button(usrname_frame, background="white", fg="black", text="Submit", command=lambda: [getusr(enter_usr), gamestartmenu()])
    submit_button.pack(padx=5, pady=5)

def getusr(usr):
    global usrname
    usrname=usr.get()
    usr.pack_forget()


def gamestartmenu():
    gamestartbuttons={"Start":gamestart, "Exit":quit, "Check Leaderboard":leaderboard, "Customize controls":choosekeys, "Load game":showgames}
    createmenu(gamestartbuttons, "Welcome", "Blue")

def leaderboard():

    lbframe=LabelFrame(window, fg="white", text="LEADERBOARD", background="red", font='Helvetica 16')
    lbframe.place(x=0, y=0, width=w, height=h)

    players=[]

    f=open('leaderboard.txt', 'r')
    for line in f.readlines():
        usr, usrscore=line.split("=")
        usrscore=int(usrscore.strip('\n'))
        players.append([usr, usrscore])
    f.close()
    players=sorted(players, key=lambda i:i[1], reverse=True)

    if len(players)<=10:
        boardentry=len(players)
    else:
        boardentry=10
    
    for i in range(boardentry):
        usr=players[i][0]
        usrscore=players[i][1]
        if usr=="":
            usr="Unknown"
        ltext=(str(i+1)+"."+usr+" scored "+str(usrscore)+"\n")
        showboard=Label(lbframe, text=ltext, fg="white", bg="red")
        showboard.pack()

    Button(lbframe, fg="black", bg="red", text="Back to Start", command=gamestartmenu).pack()

def updateldrdata():
    cur_score=int(score.cget("text"))
    f=open('leaderboard.txt', 'a')
    f.write(usrname+'='+str(cur_score)+'\n')
    f.close()

def choosekeys():
    str1=StringVar()
    str1.set(ctrlkeys[left])
    str2=StringVar()
    str2.set(ctrlkeys[right])
    keypgleft = LabelFrame(window, fg="white", text="Choose keys for movement in the left direction", background="orange")
    keypgleft.place(x=0, y=0, width=w//2, height=h)

    keypgright=LabelFrame(window, fg="white", text="Choose keys for movement in the right direction", background="orange")
    keypgright.place(x=640, y=0, width=w//2, height=h)
    keylbleft=Label(keypgleft, fg="black", width=300, height=10, text="Move left", background="orange")
    keylbleft.pack()
    keylbright=Label(keypgright, fg="black", width=980, height=10, text="Move Right", background="orange")
    keylbright.pack()
    left_choose={"Left key":"<Left>", "a key":"<a>", "w key":"<w>"}
    right_choose={"Right key":"<Right>", "d key":"<d>", "s key":"<s>"}
    for i, j in left_choose.items():
        Radiobutton(keypgleft, text=i, padx=1, pady=1, width=15, variable=str1, fg="white", background="orange", value=j, indicator=0, command=lambda: changectrl(left, str1.get())).pack()

    for i, j in right_choose.items():
        Radiobutton(keypgright, text=i, padx=1, pady=1, width=15, variable=str2, fg="white", background="orange", value=j, indicator=0, command=lambda: changectrl(right, str2.get())).pack()

    Button(keypgright, background="orange", fg="black", text="Go to Start Menu", padx=10, width=20, command=gamestartmenu).pack()

def changectrl(action, chosen_key):
    window.unbind(ctrlkeys[action])
    ctrlkeys[action] = chosen_key

def showgames():
    saved=LabelFrame(window, fg="white", text="Currently saved games", background="orange")
    saved.place(x=0, y=0, width=w, height=h)

    saved_path="./games/"

    gamelist=[]

    for i, file in enumerate(os.listdir(path=saved_path)):
        game_id=int(float(file[:-4]))
        game_id=datetime.datetime.fromtimestamp(game_id)
        gamelist.append(Button(saved, background="black", fg="white", text=game_id, width=25, height=5, command=lambda: [loadgame(file)]))
        gamelist[i].pack()

        Button(saved, background="red", fg="white", text="Go to Start Menu", width=25, height=5, command=gamestartmenu).pack()

def loadgame(file):
    global usrname
    openf="./games/"+file
    with open(openf, "r") as f:
        f_data=f.read()
        usrname=f_data.split("=")[0]
        score=f_data.split("=")[1]
    update_score(None, score)
    Misc.lift(canvas)
    posreset()
    startani()

def endgame():
    unbindkeys()
    updateldrdata()
    maincar_pos=canvas.coords(gameobjects["maincar"])
    explosion_img=PhotoImage(file="./images/rszexplosion1.png")
    explosion=canvas.create_image(maincar_pos, image=explosion_img)
    canvas.image=explosion_img
    endmes=Label(canvas, text="Sorry, you failed", fg= "yellow", font="Helvetica 50", background="black")
    endmes.pack()
    change_pause()
    window.after(3000, lambda: [canvas.delete(explosion), endmes.pack_forget(), gamestartmenu()])

def createmenu(buttons, message, colour="Blue"):
    menu = LabelFrame(window, fg="white", text="Menu", background="black")
    menu.place(x=0, y=0, width=w, height=h)

    output=Label(menu, fg=colour, height=5, text=message, background="black", font="Helvetica 16")
    output.pack

    i=[None]*len(buttons)

    for text, commands in enumerate(buttons):
        i[text]=Button(menu, background="black", fg=colour, text=commands, width=40, height=5, command=buttons[commands])
        i[text].pack()

def gamestart():
    update_score(0)
    Misc.lift(canvas)
    posreset()
    startani()

def posreset():
    global gameobjects
    try:
        canvas.delete(evilcar)
        canvas.delete(ghost)
        canvas.delete(wrench)
    except:
        pass
    create_data()
    canvas.coords(gameobjects["maincar"], 640, 600)
    createghost()

def startani():
    change_pause()
    window.after(speed, borderanimation)
    window.after(speed, tree_ani)
    window.after(speed, evilcar_ani)
    window.after(speed, bordercol)
    window.after(speed, col_evilcar)
    window.after(speed, ghost_ani)
    window.after(speed, col_ghost)
    window.after(speed, wrench_ani)
    window.after(speed, col_wrench)
    bindkeys()


def update_score(upscr=10, ldscore=0):
    global score
    cur_score=int(score.cget("text"))
    if upscr==0:
        cur_score=0
    elif upscr==None:
        cur_score=ldscore
    else:
        cur_score+=upscr

    score.configure(text=str(cur_score))

def savecurrent():
    global usrname, score
    cur_score=int(score.cget("text"))
    cur_time=datetime.datetime.now()
    timestamped=(str(cur_time.timestamp())).split('.', 1)[0]
    savetofile="./games/"+timestamped+".txt"
    with open(savetofile, "w") as f:
        f.write(usrname+"="+str(cur_score))


def create_data():
    global animation_index
    global tree_index
    global ecar_animation_index
    global ghost_animation_index
    global wrench_animation_index
    global animation_data
    global animation_data2
    global tree_data
    global tree_data2
    global ecar_data
    global ghost_data
    global wrench_data

    animation_index=0
    tree_index=0
    ecar_animation_index=0
    ghost_animation_index=0
    wrench_animation_index=0
    animation_data=[]
    animation_data2=[]
    tree_data=[]
    tree_data2=[]
    ecar_data=[]
    ghost_data=[]
    wrench_data=[]

    for i in range(0,720,10):
        animation_data.append([10, i, 50, i+100])
        animation_data2.append([1230, i, 1270, i+100])

    for i in range(0, 720, 90):
        tree_data.append([110, i])
        tree_data2.append([1150, i])

    for i in range(0, 720, 135):
        ecar_x=randint(250, 1000)
        ecar_data.append([ecar_x, i])

    for i in range(0, 720, 25):
        ghost_x=randint(250, 1000)
        ghost_data.append([ghost_x, i])

    for i in range(0,720, 55):
        wrenchx=randint(400, 600)
        wrench_data.append([wrenchx, i])

def create_evilcar():
    global ecar_animation_index
    global ecar_data
    global evilcar
    data=ecar_data[ecar_animation_index]

    evilcar=canvas.create_image(*data, image=evilcar_img)
    ecar_animation_index+=1

    if ecar_animation_index>=len(ecar_data):
        ecar_animation_index=0

def evilcar_ani():
    global ecar_animation_index
    if not pause:
        try:
            canvas.delete(evilcar)
        except:
            pass

        create_evilcar()

        window.after(speed*100, evilcar_ani)

def col_evilcar():
    global evilcar
    if collisions(gameobjects["maincar"], evilcar):
        endgame()

    if not pause:
        window.after(10, col_evilcar)

def createghost():
    global ghost_animation_index
    global ghost_data
    global ghost
    
    data=ghost_data[ghost_animation_index]
    ghost=canvas.create_image(*data, image=ghost_img)
    ghost_animation_index+=1

    if ghost_animation_index>=len(ghost_data):
        ghost_animation_index=0

def ghost_ani():
    if not pause:
        try:
            canvas.delete(ghost)
        except:
            pass

        createghost()

        window.after(speed*10, ghost_ani)

def col_ghost():
    global ghost
    global ghostmode
    if collisions(gameobjects["maincar"], ghost):
        ghostmode=True
        update_score(10)
        window.after(5000, ghost_off)
    if not pause:
        window.after(10, col_ghost)

def create_wrench():
    global wrench_animation_index
    global wrench_data
    global wrench
    data=wrench_data[wrench_animation_index]
    wrench=canvas.create_image(*data, image=wrench_img)

    wrench_animation_index+=1

    if wrench_animation_index>=len(wrench_data):
        wrench_animation_index=0

def wrench_ani():
    global wrench_animation_index
    global wrench
    if not pause:
        try:
            canvas.delete(wrench)
        except:
            pass
    
        create_wrench()

        window.after(speed*10, wrench_ani)

def col_wrench():
    global wrench
    if collisions(gameobjects["maincar"], wrench):
        update_score(100)

    if not pause:
        window.after(10, col_wrench)



def create_tree():
    global tree_data
    global tree_data2
    global tree_index
    data = tree_data[tree_index]
    data2= tree_data2[tree_index]

    if tree_index%2==0:
        global longtree1, longtree2
        longtree1=canvas.create_image(*data, image=longtree_img)
        longtree2=canvas.create_image(*data2, image=longtree_img)
    
    else:
        global darktree1, darktree2
        darktree1=canvas.create_image(*data, image=darktree_img)
        darktree2=canvas.create_image(*data2, image=darktree_img)

    tree_index+=1
    if tree_index>=len(tree_data):
        tree_index=0
def tree_ani():
    if not pause:
        global tree_index
        try:
            if tree_index%2==0:
                canvas.delete(longtree1, longtree2)

            else:
                canvas.delete(darktree1, darktree2)

        except:
            pass
        create_tree()

        window.after(speed*10, tree_ani)


def borderanimation():
    if not pause:
        global animation_index
        global animation_data2
        global animation_data
        data=animation_data[animation_index]
        data2=animation_data2[animation_index]
        if animation_index%2==0:
            canvas.create_rectangle(*data, fill="white")
            canvas.create_rectangle(*data2, fill="white")
        else:
            canvas.create_rectangle(*data, fill="red")
            canvas.create_rectangle(*data2, fill="red")
        animation_index+=1
        if animation_index>=len(animation_data):
            animation_index=0

        window.after(speed, borderanimation)

def change_pause():
    global pause
    pause=not pause


def collisions(obj1, obj2):
    obj1pos = canvas.bbox(obj1)
    obj2pos = canvas.bbox(obj2)

    if not ghostmode:
        if obj1pos[0] in range(obj2pos[0], obj2pos[2]) or obj1pos[2] in range(obj2pos[0], obj2pos[2]):
            if obj1pos[1] in range(obj2pos[1], obj2pos[3]) or obj1pos[3] in range(obj2pos[1], obj2pos[3]):
                return True
        else:
            return False

    elif ghostmode:
        return False

def bindkeys():

    global ctrlkeys

    for key, val in ctrlkeys.items():
        window.bind(val, key)

def unbindkeys():
    global ctrlkeys

    for val in ctrlkeys.values():
        window.unbind(val)

def pausemenu(event=None):
    if not pause:
        change_pause()
        unbindkeys()
        pmenubuttons={"Resume": unpause, "Exit": quit, "Go to Start/Restart":gamestartmenu, "Save Progress": savecurrent}
        createmenu(pmenubuttons, "paused")

def unpause():
    Misc.lift(canvas)
    startani()

def left(event):
    x=-30
    y=0
    canvas.move(gameobjects["maincar"], x, y)

def right(event):
    x=30
    y=0
    canvas.move(gameobjects["maincar"], x, y)

def bosskey(event=None):
    change_pause()
    bossfr=Frame(window, background="black")
    bossfr.place(x=0, y=0, width=w, height=h)

    boss_img=PhotoImage(file="./images/bosskey.png")
    bosslab=Label(bossfr, image=boss_img)

    bosslab.pack()
    bosslab.image=boss_img
    window.unbind("<Control-b>")
    window.bind("<Control-b>", bossback)

def bossback(event=None):
    window.unbind("<Control-b>")
    window.bind("<Control-b>", bosskey)
    change_pause()
    pausemenu()

def cheat(event=None):
    update_score(100)


ctrlkeys={left:"<Left>", right:"<Right>", bosskey: "<Control-b>", pausemenu:"<Control-p>", cheat:"<semicolon>"}


def bordercol():
    if collisions(gameobjects["maincar"], gameobjects["border1"]):
        endgame()
    elif collisions(gameobjects["maincar"], gameobjects["border2"]):
        endgame()
    elif collisions(gameobjects["maincar"], gameobjects["border3"]):
        endgame()
    elif collisions(gameobjects["maincar"], gameobjects["leftborder1"]):
        endgame()
    elif collisions(gameobjects["maincar"], gameobjects["leftborder2"]):
        endgame()
    elif collisions(gameobjects["maincar"], gameobjects["leftborder3"]):
        endgame()
    if not pause:
        window.after(10, bordercol)

def ghost_off():
    global ghostmode
    ghostmode=False

if __name__=="__main__":
    # Resolution
    w=1280
    h=720

    # Global variables specifying the speed of the game
    speed=20
    pause=True
    ghostmode=False
    usrname=""
    score=None

    window=Tk()
    window.geometry("1280x720")
    window.option_add('*Font', 'Helvetica 16')

    canvas=Canvas(window)
    canvas.place(x=0, h=0, width=w, height=h)

    darktree_img=PhotoImage(file="./images/rsztree.png")
    longtree_img=PhotoImage(file="./images/longtree.png")
    background_image=PhotoImage(file="./images/bgnew.png")
    maincar_image=PhotoImage(file="./images/car1.png")
    borderimg=PhotoImage(file="./images/trackbord2rot.png")
    ghost_img=PhotoImage(file="./images/ghostmode.png")
    evilcar_img=PhotoImage(file="./images/evilcar.png")
    ghost_img=PhotoImage(file="./images/ghostmode.png")
    wrench_img=PhotoImage(file="./images/wrench.png")

    background = canvas.create_image(w//2, h//2, image=background_image)

    gameobjects = {
        "border1":canvas.create_image(250, 135, image=borderimg),
        "border2":canvas.create_image(250, 370, image=borderimg),
        "border3":canvas.create_image(250, 600, image=borderimg),
        "leftborder1":canvas.create_image(1030, 135, image=borderimg),
        "leftborder2":canvas.create_image(1030, 370, image=borderimg),
        "leftborder3":canvas.create_image(1030, 600, image=borderimg),
        "maincar":canvas.create_image(640, 600, image=maincar_image)
    }

    progstart()
    window.mainloop()
