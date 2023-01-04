import tkinter
from tkinter import Frame, Canvas,Menu

gamemode=None

class Game(Frame):
       
    global w,h,cheat,cheat2,size,pause,pl1,pl2,sets,winner_point,sets_played,number_of_sets,player1_sets,player2_sets

    #Διαστάσεις Γηπέδου
    w=900
    h=700
    
    ball_size=12
    paddle_size=50
   
    ballX=400
    ballY=350

    #Μεταβλητές Που Θα χρησιμοποιηθούν μετα 
    player1 = 0
    player2 = 0
    ball = 0
    canvas = 0
    paddle1 = 0
    paddle2 = 0
    textLabel = 0
    set_winner_text=0
    played_sets_text=0

    number_of_sets=0
    sets_played=0
    player1_sets=0
    player2_sets=0

    winner_point=11
            
    paddle1X = 20
    paddle1Y = h/2

    paddle2X = w-30
    paddle2Y = h/2

    #Ταχύτητα της Μπάλας
    ballDX = 2
    ballDY = -2

    paddleSpeed =25

    player1Points = 0
    player2Points = 0
    
    pl1=0
    pl2=0

    cheat=False
    cheat2=False
    pause=True
    auto1=False
    auto2=False
    sets=False

    def __init__(self, parent):            
        Frame.__init__(self, parent)
        self.parent = parent        
        self.initUI()   

    #δημιουργία Συντομεύσεων στο Πληκτρολόγιο
    def key(self, event):  
        if gamemode=="twoplayers":
            
            if event.char == 'w' or event.char=='ς':                                              
                if self.canvas.coords(self.paddle1)[1]>=30:
                    self.canvas.move(self.paddle1,0,-self.paddleSpeed)
                 
            if event.char == 's' or event.char=='σ':
                if self.canvas.coords(self.paddle1)[3]<=h-30:
                    self.canvas.move(self.paddle1,0,self.paddleSpeed)
                    
        elif gamemode=="oneplayer":
            pass
        
        if event.char == 'p' or event.char=='π':
            if self.canvas.coords(self.paddle2)[1]>=30:                                                         
                self.canvas.move(self.paddle2,0,-self.paddleSpeed)
                
        if event.char == 'l' or event.char=='λ':
            if self.canvas.coords(self.paddle2)[3]<=h-30:
                self.canvas.move(self.paddle2,0,self.paddleSpeed)
        
        if event.char == 'q' or event.char==';':
            Exit() 
            
        if event.char==' ':
            ps()
            
        if  event.char=='n' or event.char=='ν':
            new_game()
            
        if event.char=='c' or event.char=='ψ':
            CHEAT()
            
        if  event.char=='v'or event.char=='ω':
            CHEAT2()

    #Κύρια Συνάρτηση Κίνησης
    def doMove(self):
        global pl1,pl2,sets_played,player1_sets,player2_sets
        
        try:
            if pause==False:
                self.canvas.move(self.ball,self.ballDX, self.ballDY)

            #Οριοθέτηση της Μπάλας εντός των Γραμμών 
            if self.canvas.coords(self.ball)[1] <= 20:  
                self.ballDY = -self.ballDY

            if self.canvas.coords(self.ball)[3] >= self.winHEIGHT:
                self.ballDY = -self.ballDY
                
            if self.doCollide(self.canvas.coords(self.ball),self.canvas.coords(self.paddle1)) or self.doCollide(self.canvas.coords(self.ball),self.canvas.coords(self.paddle2)):
                self.ballDX = -self.ballDX

            # Εδώ αναγνωρίζεται αν μπήκε Γκολ
            if self.canvas.coords(self.ball)[0] <= 0:
                self.ballDX = -self.ballDX             
                self.player2Points+=1
                pl2=self.player2Points
                self.canvas.delete(self.textLabel)
                #Σκορ για τα Γκολ
                self.textLabel = self.canvas.create_text(self.winWIDTH/2,10, text=str(self.player1Points)+" | "+str(self.player2Points),fill='white')
                self.canvas.coords(self.ball,self.winWIDTH/2,self.winHEIGHT/2,self.winWIDTH/2+10,self.winHEIGHT/2+10)
                
                if sets==False:               
                        self.canvas.delete(self.set_winner_text)
                        self.canvas.delete(self.played_sets_text)
                elif sets==True :
                    #Εμφάνιση του Σκορ για τα Σετ
                    self.canvas.delete(self.set_winner_text)
                    self.canvas.delete(self.played_sets_text)
                    self.set_winner_text=self.canvas.create_text(self.winWIDTH/2 +150,10,
                            text="Sets Score:"+str(player1_sets)+'l'+str(player2_sets),fill='white')
                    self.played_sets_text = self.canvas.create_text(self.winWIDTH-20,10,
                            text='Sets:'+str(sets_played),
                                                             fill='white')
                    #Έλεγχος αν έχουν εκτελεστει όλα τα Σετ
                    if self.player1Points==winner_point or self.player2Points==winner_point:
                        if number_of_sets!=sets_played:
                            if self.player1Points>self.player2Points:
                                player1_sets+=1
                            elif self.player1Points<self.player2Points:
                                player2_sets+=1                 
                            self.player1Points=0
                            self.player1Points=0
                        else:
                            if self.player1Points>self.player2Points:
                                player1_sets+=1
                            elif self.player1Points<self.player2Points:
                                player2_sets+=1
                            
                            Exit() 


            #Αντίστοιχα    
            if self.canvas.coords(self.ball)[2] >= self.winWIDTH:
                self.ballDX = -self.ballDX
                self.player1Points+=1
                pl1=self.player1Points                        
                self.canvas.delete(self.textLabel)
                self.textLabel = self.canvas.create_text(self.winWIDTH/2,10, text=str(self.player1Points)+" | "+str(self.player2Points),fill='white')
                self.canvas.coords(self.ball,self.winWIDTH/2,self.winHEIGHT/2,self.winWIDTH/2+self.ball_size,self.winHEIGHT/2+self.ball_size)
                if sets==False:               
                        self.canvas.delete(self.set_winner_text)
                        self.canvas.delete(self.played_sets_text)
                elif sets==True :
                    self.canvas.delete(self.set_winner_text)
                    self.canvas.delete(self.played_sets_text)
                    self.set_winner_text=self.canvas.create_text(self.winWIDTH/2 +150,10,
                            text="Sets Score:"+str(player1_sets)+'l'+str(player2_sets),fill='white')
                    self.played_sets_text = self.canvas.create_text(self.winWIDTH-20,10,
                            text='Sets:'+str(sets_played),
                                                             fill='white')

                    if self.player1Points==winner_point or self.player2Points==winner_point:
                        if number_of_sets!=sets_played:
                            sets_played+=1
                            if self.player1Points>self.player2Points:
                                player1_sets+=1
                            elif self.player1Points<self.player2Points:
                                player2_sets+=1
                                              
                            self.player1Points=0
                            self.player1Points=0
                        else:
                            if self.player1Points>self.player2Points:
                                player1_sets+=1
                            elif self.player1Points<self.player2Points:
                                player2_sets+=1
                            Exit()

            self.after(10, self.doMove)

            if gamemode=="oneplayer" and pause==False:
                self.after(10,self.automove_paddle1)
                
            if cheat==True:
                self.after(10,self.follow_ball_paddle2)
                self.after(10,self.follow_ball_paddle1)
                
            elif cheat2==True :
                self.after(10,self.follow_ball_paddle2)
                
        except:
            pass

    # Η Συνάρτηση  που κάνει την Ρακέτα 1 να ακολουθει το ύψος της Μπάλας
    def follow_ball_paddle1(self):
        
        try:
            #Εκχωρούνται οι Συντεταγμένες της Ρακέτας1 και της Μπάλας 
            coords_self_paddle_1 = self.canvas.coords(self.paddle1)
            coords_self_ball=self.canvas.coords(self.ball)
        except:
            pass          
       #Το Ύψος της Ρακέτας γίνεται ίδιο με το Ύψος της Μπάλας
        coords_self_paddle_1[1] = coords_self_ball[1]
        coords_self_paddle_1[3] = coords_self_ball[3]
        
        self.canvas.coords(self.paddle1,coords_self_paddle_1[0],
                           coords_self_paddle_1[1]+35,coords_self_paddle_1[2],
                           coords_self_paddle_1[3]-25)

     #Αντίστοιχα για τη Ρακέτα2         
    def follow_ball_paddle2(self):
        
        coords3 = self.canvas.coords(self.paddle2)
        coords_self_ball=self.canvas.coords(self.ball)
        coords3[1] = coords_self_ball[1] 
        coords3[3] = coords_self_ball[3]
        
        self.canvas.coords(self.paddle2,coords3[0],coords3[1]+35,coords3[2],coords3[3]-25)


    #Συνάρτηση με την οποία παίζει ο Υπολογιστής στην Λειτουργία του ενός Παίκτη   
    def automove_paddle1(self):
        try :
            coords_self_paddle_1 = self.canvas.coords(self.paddle1)
            coords_self_ball=self.canvas.coords(self.ball)
        except:
            pass

        #Η μπάλα απομακρύνεται απο την ρακέτα1 ,και εκείνη πηγαίνει στην πιο κοντινή Γωνία 
        if self.ballDX>0:
            if coords_self_paddle_1[1]>=350:
                if coords_self_paddle_1[3]<680:
                    self.canvas.move(self.paddle1,0,2)
            elif coords_self_paddle_1[1]<350:
                if coords_self_paddle_1[1]>20:
                    self.canvas.move(self.paddle1,0,-2)
        #Εαν η Μπάλα αλλάξει φορά ,η Ρακέτα ελέγχει την Σχετική της θέση με την μπάλα και κατευθυνεται προς αυτη          
        try:
            if self.ballDX<0:
                if coords_self_paddle_1[1]+(coords_self_paddle_1[3]-coords_self_paddle_1[1])/2<coords_self_ball[1]:
                    self.canvas.move(self.paddle1,0,2)
                elif coords_self_paddle_1[3]-(coords_self_paddle_1[3]-coords_self_paddle_1[1])/2>coords_self_ball[3]:
                    self.canvas.move(self.paddle1,0,-2)             
        except :
            pass

    #Εδώ οριζεται το Γήπεδο και οι ρακέτες και καλούνται οι Συναρτήσεις Κίνησης
    def initUI(self):
        global pl1,pl2
        self.parent.title("Pong")        
        self.pack(fill="both", expand=1)
        self.canvas = Canvas(self,bg='black',width=w,height=h)
        
        self.canvas.create_line(w/2,20,w/2,h-20,fill="white")
        self.canvas.create_line(20,20,20,h-20,fill="white")
        self.canvas.create_line(w-20,20,w-20,h-20,fill="white")
        self.canvas.create_line(20,20,w-20,20,fill="white")
        self.canvas.create_line(20,h-20,w-20,h-20,fill="white")
        self.canvas.pack(fill="both", expand=1)

        self.winHEIGHT = h-20
        self.winWIDTH =w-20
        self.ball = self.canvas.create_oval(0+self.ballX, 0+self.ballY, self.ball_size+self.ballX, self.ball_size+self.ballY
                                            , outline="white",fill="white", width=1)
        self.paddle1 = self.canvas.create_rectangle(0+self.paddle1X,0+self.paddle1Y, 10+self.paddle1X,
                                                    self.paddle_size+self.paddle1Y, outline="white", fill="white")
        self.paddle2 = self.canvas.create_rectangle(0+self.paddle2X,0+self.paddle2Y, 10+self.paddle2X,
                                                    self.paddle_size+self.paddle2Y, outline="white", fill="white")

        self.textLabel = self.canvas.create_text(self.winWIDTH/2,10,
                                                 text=str(self.player1Points)+" | "+str(self.player2Points),
                                                 fill="white")
        pl1=self.player1Points
        pl2=self.player2Points
        self.parent.bind("<Key>", self.key)
        self.canvas.pack(fill="both", expand=1)
        self.after(100, self.doMove)
        if gamemode=="oneplayer":
            self.after(10,self.automove_paddle1)
        if cheat==True:
            self.after(10,self.follow_ball_paddle2)
            self.after(10,self.follow_ball_paddle1)
        elif cheat2==True:
            self.after(10,self.follow_ball_paddle2)


    #Η συνάρτηση που αναγνωρίζει την Σύγκρουση της Μπάλας και της Ρακέτας
    def doCollide(self,coords_self_paddle_1,coords_self_ball):
        
        height1 = coords_self_paddle_1[3]-coords_self_paddle_1[1]
        
        width1 = coords_self_paddle_1[2]-coords_self_paddle_1[0]
        height2 = coords_self_ball[3]-coords_self_ball[1]
        width2 = coords_self_ball[2]-coords_self_ball[0]
        
        return not (coords_self_paddle_1[0] + width1 < coords_self_ball[0] or coords_self_paddle_1[1] + height1 < coords_self_ball[1] or coords_self_paddle_1[0] > coords_self_ball[0] + width2 or coords_self_paddle_1[1] > coords_self_ball[1] + height2)

#Η Κύρια Συνάρτηση    
def main():

    global gamemode,ps,Exit,root_main,CHEAT,CHEAT2,open_instructions,number_of_sets,instructions_exit,SETS,free_play,set_ting,seting_sets_1,seting_sets_2,seting_sets_3,seting_sets_4,seting_sets_5

    #Οι Συνάρτησεις για τις Μεταβλητές 
    def CHEAT():
        global cheat
        if cheat==False:
            cheat=True
        elif cheat==True:
            cheat=False

    def CHEAT2():
        global cheat2
        if cheat2==False:
            cheat2=True
        elif cheat2==True:
            cheat2=False

    #Συναρτήσεις που αφορούν τα Σετ
    def SETS():
        global sets,pause,number_of_sets
        root_gaming_mode.destroy()
        sets=True
        seting_sets()

    def free_play():
        global sets,pause
        root_gaming_mode.destroy()
        pause=False
        sets=False
       
    def set_ting():
        global sets
        if sets==False:
            sets=True
        if sets==True:
            sets=False


    #Συναρτήσεις που θέτουν συγκεκριμένο αριθμό σετ
    def seting_sets_1():
        global number_of_sets,sets,player1_sets,player2_sets,sets_played
        number_of_sets=0
        sets=True
        sets_played=0
        player2_sets=0
        player1_sets=0
        
    def seting_sets_2():
        global number_of_sets,sets,player1_sets,player2_sets,sets_played
        number_of_sets=1
        sets=True
        sets_played=0
        player2_sets=0
        player1_sets=0
        
    def seting_sets_3():
        global number_of_sets,sets,player1_sets,player2_sets,sets_played
        number_of_sets=2
        sets=True
        sets_played=0
        player2_sets=0
        player1_sets=0
        
    def seting_sets_4():
        global number_of_sets,sets,player1_sets,player2_sets,sets_played
        number_of_sets=3
        sets=True
        sets_played=0
        player2_sets=0
        player1_sets=0
        
    def seting_sets_5():
        global number_of_sets,sets,player1_sets,player2_sets,sets_played
        number_of_sets=4
        sets=True
        sets_played=0
        player2_sets=0
        player1_sets=0

    # Συνάρτηση για την Παύση 
    def ps():
        global pause
        if pause==False:
            pause=True
        elif pause==True:
            pause=False
            
    def winner():
        global WINNER ,points
        if sets==False:
            p1=pl1
            p2=pl2
        elif sets==True:
            p1=player1_sets
            p2=player2_sets
        if p2>p1:
            WINNER='Player2'
            points=p2
        elif p2<p1:
            WINNER='Player1'
            points=p1
        elif p2==p1:
            WINNER='Draw'
            points=p1
        
    # Οριζούμε τη συνάρτηση που κάνει Έξοδο απο το Παράθυρο Ανακοίνωσης του Νικητή αν πατηθεί το Πλήκτρο <ENTER>
    def the_key_return(event):
        global root_exit
        if event.keysym=='Return':
            root_exit.destroy()

    #Παραθύρο Εξόδου Συνάρτησης
    def Exit():
        global root_exit
        root_main.destroy()
        winner()
        root_exit=tkinter.Tk()
        root_exit.configure(bg='black')
        frame_exit=tkinter.Frame(root_exit,relief='ridge',borderwidth=5,bg='black')
        frame_exit.pack()
        root_exit.title(string='Finished')
        #Ανάλογα Με το αν έχουμε Παίξει με Σετ ή όχι 
        if sets==False:
            if WINNER!='Draw': 
                label_exit_winner = tkinter.Label(frame_exit, text=str('The Winner is '+str(WINNER)+' with '+str(points)+' points.' ),
                                                  font='Arial 20',fg='white',bg='black')
            else:
                label_exit_winner = tkinter.Label(frame_exit, text=str('The Game Ends with a  DRAW at '+str(points)+' points.' ),font='Arial 20',
                                                  fg='white',bg='black')
            label_exit_winner.pack(fill="both", expand=1)
        elif sets==True:
            if WINNER!='Draw': 
                label_exit_winner = tkinter.Label(frame_exit, text=str('The Winner is '+str(WINNER)
                                                      +' with '+str(points)+' sets.' ),font='Arial 20',fg='white',bg='black')
            else:
                label_exit_winner = tkinter.Label(frame_exit, text=str('The Game Ends with a  DRAW at '+str(points)+' sets.' ),font='Arial 20',
                                                  fg='white',bg='black')
            label_exit_winner.pack(fill="both", expand=1)
        button=tkinter.Button(text='EXIT?',font='Arial 20', command=root_exit.destroy)
        button.configure(bg='black',fg='white')
        button.pack(fill="both",expand=1)
        button_play_again=tkinter.Button(text='Play Again?',font='Arial 20',command=play_again,fg='white',bg='black')
        button_play_again.pack(fill="both",expand=1)
        root_exit.bind("<Return>", the_key_return)
        
        root_exit.geometry('500x150+600+300')
        root_exit.overrideredirect(True)

        root_exit.lift()
        root_exit.attributes("-topmost", True)
        root_exit.resizable(False,False)
        root_exit.mainloop()
            
        
    def open_instructions():
        global pause,root_instructions
        instructions=open('instructions.txt','r',encoding='utf-8')
        
        pause=True
        root_instructions=tkinter.Tk()
        root_instructions.configure(bg='black')
        frame2=tkinter.Frame(root_instructions,relief='ridge',borderwidth=1,bg='black')
        frame2.pack()
        root_instructions.title(string='INSTRUCTIONS')
        label = tkinter.Label(frame2, text='Instructions',font='Arial 20',
                              fg='white',bg='black')
        label.pack(fill="x", expand=1)
        instruction_text=tkinter.Text(root_instructions)
        instruction_text.insert("insert",instructions.read())
        instruction_text.config(font='Arial 16',fg='white',bg='black')
        instruction_text.pack(fill="both",expand=1)
        button_inst=tkinter.Button(text='Back to Game',font='Arial 20', command=instructions_exit)
        button_inst.configure(bg='black',borderwidth=1,fg='white')
        button_inst.pack(fill="x",expand=1)
        root_instructions.geometry('500x700+200+0')        
        root_instructions.resizable(False,False)
        instructions.close()
        
    def instructions_exit():
            global pause,root_instructions
            root_instructions.destroy()
            pause=False


    def open_credits():
        global pause,root_credits
        creds=open('credits.txt','r',encoding='utf-8')
        
        pause=True
        root_credits=tkinter.Tk()
        root_credits.configure(bg='black')
        frame=tkinter.Frame(root_credits,width=200,height=200,relief='ridge',borderwidth=5,bg='black')
        frame.pack()
        root_credits.title(string='CREDITS')
        label = tkinter.Label(frame, text='Credits',font='Arial 20',
                              fg='white',bg='black')
        label.pack(fill="x", expand=1)
        creds_text=tkinter.Text(frame)
        creds_text.insert("insert",creds.read())
        creds_text.config(width=40,height=15,font='Arial 16',fg='white',bg='black')
        creds_text.pack(fill="x",expand=1)
        button_cred=tkinter.Button(frame,text='Back to Game',font='Arial 20',
                              command=credits_exit,)
        button_cred.configure(bg='black',borderwidth=1,fg='white')
        button_cred.pack(fill="x",expand=1)
        root_credits.geometry('400x450+700+0')        
        root_credits.resizable(False,False)
        creds.close()


    def credits_exit():
            global pause,root_credits
            root_credits.destroy()
            pause=False


    root_main = tkinter.Tk()

    menubar = Menu(root_main)

    
    pong=Game(root_main)

     
    menu = Menu(menubar, tearoff = 0) 
    menubar.add_cascade(label ='menu', menu = menu)
    
    menu.add_command(label ='1 player', command = new_onep)
    menu.add_command(label ='2 players', command =new_twop)
    menu.add_separator() 
    menu.add_command(label='New Game',command=new_game)

    
    sets_menu=Menu(menubar,tearoff=0)
    menubar.add_cascade(label='sets',menu=sets_menu)
    sets_menu.add_command(label='Sets On/Off',command=set_ting)
    sets_menu.add_separator()
    sets_menu.add_command(label='1 set',command=seting_sets_1)
    sets_menu.add_command(label='2 set',command=seting_sets_2)
    sets_menu.add_command(label='3 set',command=seting_sets_3)
    sets_menu.add_command(label='4 set',command=seting_sets_4)
    sets_menu.add_command(label='5 set',command=seting_sets_5)


    prizes=Menu(menubar,tearoff=0)
    menubar.add_cascade(label="prizes",menu=prizes)
    prizes.add_command(label='Endless Show On',command=CHEAT) 


    helping=Menu(menubar,tearoff=0)
    menubar.add_cascade(label="help",menu=helping)
    helping.add_command(label='instructions',command=open_instructions)
    helping.add_command(label='credits',command=open_credits)


    menubar.add_command(label='pause',command=ps)
    menubar.add_command(label='EXIT',command=Exit)
    

    root_main.config(menu=menubar)
    root_main.geometry('{}x{}+300+40'.format(w,h))
    root_main.resizable(False,False)
    root_main.mainloop()
    menubar.mainloop()



def new_game():
    root_main.destroy()
    pause=False
    main()


def play_again():
    global pause
    root_exit.destroy()
    pause=True
    startup()
    pause=True
    main()
    
    
def new_onep():
    global gamemode,pause
    gamemode='oneplayer'
    pause=False
    root_main.destroy()
    main()

    
def new_twop():
    global gamemode,pause
    gamemode='twoplayers'
    pause=False
    root_main.destroy()
    main()

    
def onep():
    global gamemode,pause
    gamemode='oneplayer'  
    root_startup.destroy()

   
def twop():
    global gamemode,pause
    gamemode='twoplayers'
    root_startup.destroy()


def choice1():
    onep()
    gaming_mode()
    
def choice2():
    twop()
    gaming_mode()


#Αρχικό Παράθυρο Επιλογής Παικτών 
def startup():
    global root_startup
    root_startup=tkinter.Tk()
    root_startup.configure(bg='black')
    frame=tkinter.Frame(root_startup,relief='ridge',borderwidth=5,bg='black')
    frame.pack()
    root_startup.title(string='GS')
    label = tkinter.Label(frame, text="Choose gaming mode",font='Arial 20',fg='white',bg='black')
    label.pack(fill="x", expand=1)
    button1=tkinter.Button(text='oneplayer',font='Arial 20', command=choice1)
    button1.configure(bg='black',borderwidth=2,fg='white')
    button1.pack(fill="both",expand=1)
    button2=tkinter.Button(text='twoplayers ',font='Arial 20', command=choice2)
    button2.configure(bg='black',borderwidth=2,fg='white')
    button2.pack(fill="both", expand=1)
    root_startup.geometry('350x200+600+300')
    root_startup.overrideredirect(True)
    root_startup.resizable(False,False)

#Παράθυρο Επιλογής Αν θέλει ο Χρήστης να παίξει με Σετ ή όχι
def gaming_mode():
    global root_gaming_mode
    root_gaming_mode=tkinter.Tk()
    root_gaming_mode.configure(bg='black')
    frame=tkinter.Frame(root_gaming_mode,relief='ridge',borderwidth=5,bg='black')
    frame.pack()
    root_gaming_mode.title(string='Sets?')
    label = tkinter.Label(frame, text="How do you want to play?",font='Arial 20',fg='white',bg='black')
    label.pack(fill="x", expand=1)
    button1=tkinter.Button(text='Set',font='Arial 20', command=SETS)
    button1.configure(bg='black',borderwidth=2,fg='white')
    button1.pack(fill="both",expand=1)
    button2=tkinter.Button(text='Free play ',font='Arial 20', command=free_play)
    button2.configure(bg='black',borderwidth=2,fg='white')
    button2.pack(fill="both", expand=1)
    root_gaming_mode.geometry('350x200+600+300')
    root_gaming_mode.overrideredirect(True)
    root_gaming_mode.resizable(False,False)

#Παράθυρο Επιλογής με πόσα Σετ Θα παίξει ο Χρήστης
def seting_sets():
    global root_seting_sets,sets
    root_seting_sets=tkinter.Tk()
    root_seting_sets.configure(bg='black')
    frame_seting_sets=tkinter.Frame(root_seting_sets,relief='ridge',borderwidth=5,bg='black')
    frame_seting_sets.pack()
    root_seting_sets.title(string='Sets?')
    label_seting_sets = tkinter.Label(frame_seting_sets, text="How many sets?"
                          ,font='Arial 20',fg='white',bg='black')
    label_seting_sets.pack(fill="x", expand=1)
    
    button_set_1=tkinter.Button(text='One Set',font='Arial 20', command=seting_sets_1_start)
    button_set_1.configure(bg='black',borderwidth=2,fg='white')
    button_set_1.pack(fill="both",expand=1)
    
    button_set_2=tkinter.Button(text='Two Sets ',font='Arial 20', command=seting_sets_2_start)
    button_set_2.configure(bg='black',borderwidth=2,fg='white')
    button_set_2.pack(fill="both", expand=1)
    
    button_set_3=tkinter.Button(text='Three Sets ',font='Arial 20', command=seting_sets_3_start)
    button_set_3.configure(bg='black',borderwidth=2,fg='white')
    button_set_3.pack(fill="both", expand=1)
    
    button_set_4=tkinter.Button(text='Four Sets ',font='Arial 20', command=seting_sets_4_start)
    button_set_4.configure(bg='black',borderwidth=2,fg='white')
    button_set_4.pack(fill="both", expand=1)

    button_set_5=tkinter.Button(text='Five sets ',font='Arial 20', command=seting_sets_5_start)
    button_set_5.configure(bg='black',borderwidth=2,fg='white')
    button_set_5.pack(fill="both", expand=1)

    root_seting_sets.geometry('350x500+600+200')
    root_seting_sets.overrideredirect(True)
    root_seting_sets.resizable(False,False)

#Αρχικές Συναρτήσεις που καθορίζουν πόσα Σετ Θα παίξει ο Χρήστης στην seting_sets
def seting_sets_1_start():
    global number_of_sets,pause
    number_of_sets=0
    root_seting_sets.destroy()
    pause=False
    
def seting_sets_2_start():
    global number_of_sets,pause
    number_of_sets=1
    root_seting_sets.destroy()
    pause=False

def seting_sets_3_start():
    global number_of_sets,pause
    number_of_sets=2
    root_seting_sets.destroy()
    pause=False

def seting_sets_4_start():
    global number_of_sets,pause
    number_of_sets=3
    root_seting_sets.destroy()
    pause=False

def seting_sets_5_start():
    global number_of_sets,pause
    number_of_sets=4
    root_seting_sets.destroy()
    pause=False



if __name__ == '__main__':   
    startup()
    main()
    
