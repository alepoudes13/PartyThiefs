import random
import arcade
import os
import math

# --- Constants ---
SCREEN_WIDTH=480
SCREEN_HEIGHT=480
SCORE_WIDTH=1300
SCORE_HEIGHT=650

SPRITE_SCALING_PLAYER=0.5
SPRITE_SCALING_PART=0.4
SPRITE_SCALING_ENEMY=0.6

speed_x=[]
speed_y=[]
enem_speed_x=[]
enem_speed_y=[]

MOVEMENT_SPEED = 5

#---Variables
open_score=False
score=0
upper={" ":" ","1":"!","2":"@","3":"#","4":"$","5":"%","6":"^","7":"&","8":"*","9":"(","0":")","-":"_",
"=":"+",";":":","'":"\"",",":"<",".":">","/":"?","[":"{","]":"}","\\":"|"
}

class MyGame(arcade.Window):
    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Party thiefs")

        self.player_sprite=None
        self.enemy_sprite=None
        self.part_sprite=None

        self.part_xy=[]
        self.enemy_xy=[]
        self.part_rgb=[]
        self.player_xy=[100,100]
        self.background=None
        self.score=0
        self.setup_background=100

        self.pressed=False
        self.mouse_x=0
        self.mouse_y=0
        self.part_count=30

        arcade.set_background_color(arcade.color.BLACK)


    def setup(self):

        # Sprite lists

        self.player_sprite=arcade.Sprite("images/character_party.png",SPRITE_SCALING_PLAYER)
        self.enemy_sprite=arcade.SpriteList()
        self.enemy_sprite.append(arcade.Sprite("images/enemy.png",SPRITE_SCALING_ENEMY))
        self.part_sprite=arcade.SpriteList()
        self.part_sprite.append(arcade.Sprite("images/light_blue_part.png",SPRITE_SCALING_PART))

        self.score=0
        self.click_wait=0
        self.pause_on=False
        self.pause_wait=0
        self.background=arcade.Sprite("images/party thiefs.png",1)
        self.background.center_x=240
        self.background.center_y=240

        for i in range(self.part_count):
            part=[random.randrange(SCREEN_WIDTH),random.randrange(SCREEN_HEIGHT)]

            sp_x=random.randrange(-480,480)/100-2.4
            sp_y=random.randrange(-480,480)/100-2.4

            speed_x.append(sp_x)
            speed_y.append(sp_y)

            rgb=(random.randint(0,255),random.randint(0,255),random.randint(0,255))

            self.part_rgb.append(rgb)
            self.part_xy.append(part)

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        if self.setup_background>0:
            arcade.start_render()
            self.background.draw()
            self.setup_background-=1
        elif self.part_count>0:
            """ Render the screen """
            arcade.start_render()
            arcade.draw_rectangle_filled(self.player_xy[0],self.player_xy[1],10,10,arcade.color.BLACK)
            for iter,part in enumerate(self.part_xy):
                arcade.draw_rectangle_filled(part[0],part[1],7,7,self.part_rgb[iter])
            for enemy in self.enemy_xy:
                arcade.draw_rectangle_filled(enemy[0],enemy[1],15,15,arcade.color.WHITE)

            # Put the text on the screen.
            output = f"Score: {self.score}"
            arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        elif self.part_count<=0:
            arcade.start_render()
            file=open("files/hscore.txt","r")
            hscore=int(file.read())
            hscore=hscore if hscore>self.score else self.score
            score = f"   Score: {self.score}\nHigh score: {hscore}"
            arcade.draw_text(score, 145, 250, arcade.color.WHITE, 30)
            file.close()
            file=open("files/hscore.txt","w")
            file.write(str(hscore))
            file.close()
            text=f"Press X to close game or T to open score table"
            arcade.draw_text(text,10,20,arcade.color.WHITE, 14)

    def on_mouse_motion(self,x,y,dx,dy):
        if self.pause_on==False:
            self.player_xy=[x,y]

    def on_mouse_drag(self,x,y,dx,dy,buttons,modifiers):
        if self.pause_on==False:
            if self.click_wait==0:
                self.pressed=True
                self.mouse_x=x
                self.mouse_y=y
                self.player_xy=[x,y]

    def on_mouse_press(self,x,y,button,modifiers):
        if self.pause_on==False:
            if self.click_wait==0:
                self.pressed=True
                self.mouse_x=x
                self.mouse_y=y
                self.player_xy=[x,y]

    def on_mouse_release(self,x,y,button,modifiers):
        self.pressed=False

    def on_key_press(self,key,modifiers):
        if self.part_count<=0:
            if key==arcade.key.X:
                arcade.close_window()
            elif key==arcade.key.T:
                global open_score
                open_score=True
                global score
                score=self.score
                arcade.close_window()
        else:
            if key==arcade.key.P and self.pause_wait==0:
                if self.pause_on==True:
                    self.pause_wait=100
                    self.pause_on=False
                else:
                    self.pause_on=True

    def update(self, delta_time):
        if self.setup_background>0:
            a=1
        elif self.part_count>0:
            if self.pause_on==False:

                if self.pause_wait>0:
                    self.pause_wait-=1

                if self.click_wait>0:
                    self.pressed=False
                    self.click_wait-=1

                self.player_sprite.center_x=self.player_xy[0]
                self.player_sprite.center_y=self.player_xy[1]

                for iter,part in enumerate(self.part_xy):
                    self.part_xy[iter][0]+=speed_x[iter]
                    self.part_xy[iter][1]+=speed_y[iter]
                    x=self.part_xy[iter][0]
                    y=self.part_xy[iter][1]
                    if x<=0:
                        self.part_xy[iter][0]+=SCREEN_WIDTH
                    elif x>=SCREEN_WIDTH:
                        self.part_xy[iter][0]-=SCREEN_WIDTH
                    if y<=0:
                        self.part_xy[iter][1]+=SCREEN_HEIGHT
                    elif y>=SCREEN_HEIGHT:
                        self.part_xy[iter][1]-=SCREEN_HEIGHT

                    if self.pressed==True:
                        d=math.sqrt(math.pow(x-self.mouse_x,2)+math.pow(y-self.mouse_y,2))
                        self.part_xy[iter][0]+=9*(self.mouse_x-x)/d
                        self.part_xy[iter][1]+=9*(self.mouse_y-y)/d

                for iter,enemy in enumerate(self.enemy_xy):
                    self.enemy_xy[iter][0]+=enem_speed_x[iter]
                    self.enemy_xy[iter][1]+=enem_speed_y[iter]
                    if self.enemy_xy[iter][0]<=0:
                        self.enemy_xy[iter][0]+=SCREEN_WIDTH
                    elif self.enemy_xy[iter][0]>=SCREEN_WIDTH:
                        self.enemy_xy[iter][0]-=SCREEN_WIDTH
                    if self.enemy_xy[iter][1]<=0:
                        self.enemy_xy[iter][1]+=SCREEN_HEIGHT
                    elif self.enemy_xy[iter][1]>=SCREEN_HEIGHT:
                        self.enemy_xy[iter][1]-=SCREEN_HEIGHT

                self.count=0
                for part in self.part_xy:
                    self.part_sprite[0].center_x=part[0]
                    self.part_sprite[0].center_y=part[1]
                    part_caught=arcade.check_for_collision_with_list(self.player_sprite,self.part_sprite)
                    if part_caught.__len__()>0 and self.pressed==True:
                        self.count+=1

                if self.count==self.part_count:
                    enemy=[random.randrange(SCREEN_WIDTH),random.randrange(SCREEN_HEIGHT)]

                    sp_x=random.randrange(-480,480)/25-2.4
                    sp_y=random.randrange(-480,480)/25-2.4

                    enem_speed_x.append(sp_x)
                    enem_speed_y.append(sp_y)

                    self.enemy_xy.append(enemy)
                    self.click_wait=20
                    self.pressed=False
                    self.score+=1


                self.count=0
                for enemy in self.enemy_xy:
                    self.enemy_sprite[0].center_x=enemy[0]
                    self.enemy_sprite[0].center_y=enemy[1]
                    fight=arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprite)
                    if fight.__len__()>0 and self.pressed==True:
                        self.count+=1
                        break
                if self.count>0 and self.pressed==True:
                    if speed_x.__len__()>0:
                        for i in range(3):
                            speed_x.pop()
                            speed_y.pop()
                            self.part_xy.pop()
                            self.part_rgb.pop()

                    self.part_count-=3
                    self.click_wait=2

class Score(arcade.Window):
    def __init__(self):
        super().__init__(SCORE_WIDTH, SCORE_HEIGHT, "Score table")

        self.caps_on=False
        self.shift_on=False
        self.stage=0
        self.player_list=None
        self.score=0
        self.nickname=""
        self.stars=""
        self.password=""
        self.exist=False

    def setup(self):
        global score
        self.score=score
        with open("files/table.txt","r") as f:
            self.player_list=f.readlines()
            for iter,line in enumerate(self.player_list):
                count,*name=line.split(' ')
                name=list(name)
                name='_'.join(name)
                name=name[0:name.__len__()-1]
                count=int(count)
                self.player_list[iter]=(count,name)

    def on_draw(self):
        arcade.start_render()
        if self.stage==0:
            output=f"Enter a nickname: {self.nickname}\nEnd typing with `"
            arcade.draw_text(output,10,615,arcade.color.WHITE,40)
        if self.stage==1:
            for cont in self.player_list:
                if self.nickname in cont:
                    output=f"This nickname already exists. Do you want to change it?(Yes-1,No-0)"
                    arcade.draw_text(output,10,622,arcade.color.WHITE,30)
                    self.stage=2
                    self.exist=True
                    break
            if self.exist==False:
                self.stage=4

        if self.stage==2:
            output=f"This nickname already exists. Do you want to change it?(Yes-1,No-0)"
            arcade.draw_text(output,10,622,arcade.color.WHITE,30)

        if self.stage==3:
            if self.nickname!="Admin":
                self.stage=4
            else:
                output=f"Enter admin's password: {self.stars}\nEnd typing with `"
                arcade.draw_text(output,10,622,arcade.color.WHITE,30)

        if self.stage==5:
            with open("files/table.txt","w") as f:
                for cont in self.player_list:
                    string=" ".join((str(cont[0]),cont[1]))
                    string+="\n"
                    f.writelines(string)
                self.stage=6
            with open("files/table.txt","r") as f:
                self.player_list=f.readlines()
                for iter,line in enumerate(self.player_list):
                    count,*name=line.split(' ')
                    name=list(name)
                    name='_'.join(name)
                    name=name[0:name.__len__()-1]
                    self.player_list[iter]=(count,name)

        if self.stage==6:
            self.x=10
            self.y=630
            for cont in self.player_list:
                line="*" * (31-cont[0].__len__()-cont[1].__len__())
                output=f"{line.join((cont[1],cont[0]))}"
                arcade.draw_text(output,self.x,self.y,arcade.color.WHITE,15)
                self.y-=17
                if self.y<=40:
                    self.y=630
                    self.x+=330
            output=f"Press X to close window"
            arcade.draw_text(output,1100,10,arcade.color.WHITE,10)

    def on_key_press(self,key,modifiers):
        if key==arcade.key.CAPSLOCK:
            if self.caps_on==False:
                self.caps_on=True
            else:
                self.caps_on=False
        if key==arcade.key.LSHIFT or key==arcade.key.RSHIFT:
            self.shift_on=True
        if self.stage==0 and self.nickname.__len__()<24:
            if key>=ord('a') and key<=ord('z'):
                symbol=chr(key)
                if not(self.caps_on==self.shift_on):
                    symbol=symbol.upper()
                self.nickname+=symbol
            elif chr(key) in upper:
                symbol=chr(key)
                if self.shift_on==True:
                    symbol=upper[symbol]
                self.nickname+=symbol
            if key==arcade.key.GRAVE:
                self.stage=1
                self.nickname=self.nickname.replace(" ","_")
            if key==arcade.key.BACKSPACE:
                if self.nickname.__len__()>0:
                    nick=list(self.nickname)
                    nick.pop()
                    self.nickname=''.join(nick)
        elif self.stage==2:
            if key==arcade.key.KEY_1:
                self.stage=0
                self.nickname=""
                self.exist=False
            elif key==arcade.key.KEY_0:
                self.stage=3

        elif self.stage==3:
            if key>=ord('a') and key<=ord('z'):
                symbol=chr(key)
                if not(self.caps_on==self.shift_on):
                    symbol=symbol.upper()
                self.password+=symbol
                self.stars+="*"
            elif chr(key) in upper:
                symbol=chr(key)
                if self.shift_on==True:
                    symbol=upper[symbol]
                self.password+=symbol
                self.stars+="*"
            if key==arcade.key.BACKSPACE:
                if self.password.__len__()>0:
                    passw=list(self.password)
                    passw.pop()
                    self.password=''.join(passw)
                    star=list(self.stars)
                    star.pop()
                    self.stars=''.join(star)
            if key==arcade.key.GRAVE:
                if self.password=="Krabsburger01":
                    self.stage=4
                else:
                    self.stage=1
                    self.password=""
                    self.stars=""
        elif self.stage==6:
            if key==arcade.key.X:
                arcade.close_window()

    def on_key_release(self,key,modifiers):
        if key==arcade.key.LSHIFT or key==arcade.key.RSHIFT:
            self.shift_on=False

    def update(self,delta_time):
        if self.stage==4:
            if self.exist==True:
                for iter,cont in enumerate(self.player_list):
                    if cont[1]==self.nickname:
                        best_scr=max(cont[0],self.score)
                        self.player_list[iter]=(best_scr,self.nickname)
                        break
            else:
                self.player_list.append((self.score,self.nickname))
            self.player_list=reversed(sorted(self.player_list))
            self.stage=5

def main():

    window = MyGame()
    window.setup()
    arcade.run()
    if open_score==True:
        window=Score()
        window.setup()
        arcade.run()

if __name__ == "__main__":
    main()
