 # TWSIAM演講時間
from ast import While
from lib2to3.pytree import convert
import os,time
import pygame as pg
from pyparsing import White, line  
from pygame.locals import *
from sys import exit

model_time=3000
mult=1                                         #初始畫面大小倍數
mult_compare=2                                 #全螢幕之後放大比例(改)
FPS = 10
WIDTH_init = 1290*mult
HEIGHT_init = 690*mult
SCREEN_SIZE = (WIDTH_init, HEIGHT_init)
count=0 

#顏色
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)

#警告語  (改)
slogan1='QA'
slogan2='時間到'

#顏色
start_word_color=(255,255,255)                  #開始畫面字
backgroung_color_normal=GREEN                   #倒數計時背景(白)
backgroung_color_countdown1=YELLOW              #倒數計時背景1(警告時)(綠)
backgroung_color_countdown2=RED                 #倒數計時背景2(警告時)
#backgroung_color_countdown3=BLACK               #倒數計時背景3(警告時)
word_color=(0,0,0)                              #介面字
remaining_number_color_normal=BLACK             #倒數計時的數字(黑)
remaining_number_color_countdown1=BLACK         #倒數計時的數字1(警告時)(紅)
remaining_number_color_countdown2=BLACK         #倒數計時的數字2(警告時)
#remaining_number_color_countdown3=WHITE         #倒數計時的數字3(警告時)

#倒數計時模式
speech_model=[2700,300,-300]                   #50分鐘\5分鐘\5分鐘

#字體大小
word_size=int(22*mult)
word_title_size=int(42*mult)
line_space_size=int(10*mult)
number_size=int(400*mult)                


# 視窗初始化and創建視窗
pg.init()
screen = pg.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
pg.mixer.init()
# screen1 = pg.display.set_mode((WIDTH_init, HEIGHT_init))  # 視窗大小
pg.display.set_caption("演講時間")
clock = pg.time.Clock()

#載入圖片
logo_img=pg.image.load(os.path.join("TWSIAM","logo.png")).convert()
logo_img=pg.transform.scale(logo_img,(50,50))
pg.display.set_icon(logo_img)  #左邊開始的小圖案

#計算今天是第幾天
schedule_time=(((int(time.time())+28800)//86400)+3)%7+1 

#現在時間
week=['一','二','三','四','五','六','日']
time1=time.localtime()
today_moment="西元"+str(int(time1.tm_year))+"年"
today_moment+=str(time1.tm_mon)+"月"+str(time1.tm_mday)+"日"
today_moment+="   星期"+week[int(schedule_time)-1]
 
#載入字體
font_name=os.path.join("TWSIAM","font.ttf")   

def draw_text(surf,text,size,x,y,colar):        #顯示資訊 
    font=pg.font.Font(font_name,size)
    text_surface=font.render(text,True,colar)   #第二個參數使用TRUE,會使字體比較滑順
    text_rect=text_surface.get_rect()
    text_rect.x=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def prune(str):    #修剪最後面的空格
    x=list(str)
    del x[len(str)-1:len(str)]
    str="".join(x)
    return str

def draw_init():      #初始畫面顯示的資訊
    draw_text(screen,"歡迎使用",word_title_size,(WIDTH_init/2)-2*word_title_size,HEIGHT_init/4,start_word_color)
    draw_text(screen,"按任意鍵以繼續",word_size,(WIDTH_init/2)-word_size*(3.5),HEIGHT_init/2,start_word_color)
    pg.display.update()
    waiting=True 
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pg.event.get():           
            if event.type == pg.QUIT:         #如果按叉叉就把視窗關掉
                pg.quit()
                return True
            elif event.type == pg.KEYUP:      #如果按鍵盤就進入主畫面
                waiting=False
                return False
            elif event.type == pg.MOUSEBUTTONUP:      #如果按滑鼠就進入主畫面
                waiting=False
                return False

all_sprites = pg.sprite.Group()

# 畫面迴圈
show_init=True
running = True
while running: 
    if show_init:
        close=draw_init()
        time_start=time.localtime()
        if close:
            break
        show_init=False
    
    clock.tick(FPS)  # 一秒最多運行FPS次

    # 取得輸入
    for event in pg.event.get():
        if event.type == VIDEORESIZE:     # get the size of the window
            SCREEN_SIZE = event.size      # set the mode of the window
            screen = pg.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
        if event.type == pg.QUIT:         #如果按叉叉就把視窗關掉
            running = False
        elif event.type==pg.KEYDOWN:      #如果按鍵盤
            if event.key==pg.K_ESCAPE:    #按esc也會退出
                running = False
            elif event.key==pg.K_SPACE:
                running = False

    WIDTH, HEIGHT= SCREEN_SIZE
    # zoom_mult=int((WIDTH/WIDTH_init)+(HEIGHT/HEIGHT_init))/2
    zoom_mult=2                         #改
    word_size=int(11.76*zoom_mult)
    word_title_size=int(22.45*zoom_mult)
    line_space_size=int(5.34*zoom_mult)
    number_size=int(213.9*zoom_mult) 
    # 更新視窗
    all_sprites.update()
    #現在時刻
    now=time.localtime()
    hour=str(now.tm_hour)
    min=str(now.tm_min)
    sec=str(now.tm_sec)

    if len(hour)==1:
        hour='0'+hour   
    if len(min)==1:
        min='0'+min
    if len(sec)==1:
        sec='0'+sec
    now_moment=today_moment+'   '+hour+':'+min+':'+sec

    time1=time.localtime()
    now_sec=time1.tm_hour*3600+time1.tm_min*60+time1.tm_sec
    start_sec=time_start.tm_hour*3600+time_start.tm_min*60+time_start.tm_sec
    speech_time=int(model_time) #這個活動的時間有多長   
    remaining_time_sec=start_sec-now_sec+int(speech_model[0])+model_time*count  #一開始count=0
    if remaining_time_sec<=speech_model[2]:
        count+=1
    x=str(int(remaining_time_sec)//60)
    y=str(int(remaining_time_sec)%60)
    if len(x)==1:
        x='0'+x
    if len(y)==1:
        y='0'+y
    remaining_time=x+':'+y
    speech_remaing_time1=speech_model[0]
    speech_remaing_time2=speech_model[1]
    speech_remaing_time3=speech_model[2]
    #speech_remaing_time4=speech_model[3]
        
    #畫面顯示
    if remaining_time_sec<=speech_remaing_time1 and remaining_time_sec>speech_remaing_time2: 
        screen.fill(backgroung_color_normal)
        draw_text(screen,str(remaining_time),number_size,WIDTH/2-number_size*(5/4),HEIGHT/2-number_size*(5/8),remaining_number_color_normal)   
    elif remaining_time_sec<=speech_remaing_time2 and remaining_time_sec>0:
        screen.fill(backgroung_color_countdown1)
        draw_text(screen,str(remaining_time),number_size,WIDTH/2-number_size*(5/4),HEIGHT/2-number_size*(5/8),remaining_number_color_countdown1)
    else:  #改這裡
        remaining_time_sec=start_sec-now_sec+int(speech_model[0])+model_time*count
        remaining_time_sec=-1*int(speech_remaing_time3)+remaining_time_sec
        x=str(int(remaining_time_sec)//60)
        y=str(int(remaining_time_sec)%60)
        if len(x)==1:
            x='0'+x
        if len(y)==1:
            y='0'+y
        remaining_time=x+':'+y
        screen.fill(backgroung_color_countdown2)
        # draw_text(screen,str(remaining_time),number_size,WIDTH/2-number_size*(5/4),HEIGHT/2-number_size*(5/8),remaining_number_color_countdown2)
        slogan_word_size=int(number_size*(8/10))                                                                                                #(改)
        draw_text(screen,slogan1,slogan_word_size,WIDTH/2-slogan_word_size*(0.8),HEIGHT*(1/3)-slogan_word_size*(1/2),remaining_number_color_countdown2)   #QA

        slogan_word_number_size=int(HEIGHT-(HEIGHT*(1/3)-slogan_word_size*(1/2))-slogan_word_size-4*line_space_size)
        draw_text(screen,str(remaining_time),slogan_word_number_size,WIDTH/2-slogan_word_number_size*(5/4),HEIGHT-3*line_space_size-slogan_word_number_size,remaining_number_color_countdown2)   #數字  
        
    all_sprites.draw(screen)
    draw_text(screen,str(now_moment),word_size+15,line_space_size,line_space_size,word_color)
    pg.display.update()
pg.quit()
