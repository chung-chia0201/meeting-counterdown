 # TWSIAM演講時間
from ast import While
from lib2to3.pytree import convert
import os,time
import pygame as pg
from pyparsing import White, line  
from pygame.locals import *
from sys import exit

mult=1                                         #初始畫面大小倍數(改)
mult_compare=2                                 #全螢幕之後放大比例(改)
FPS = 10
WIDTH_init = 1290*mult
HEIGHT_init = 690*mult
SCREEN_SIZE = (WIDTH_init, HEIGHT_init)

#顏色
start_word_color=(255,255,255)                  #開始畫面字
backgroung_color_normal=(255,255,255)           #倒數計時背景
backgroung_color_countdown1=(0,255,0)           #倒數計時背景1(警告時)
backgroung_color_countdown2=(255,0,0)           #倒數計時背景2(警告時)
word_color=(0,0,0)                              #介面字
remaining_number_color_normal=(0,0,0)           #倒數計時的數字
remaining_number_color_countdown1=(255,0,0)     #倒數計時的數字1(警告時)
remaining_number_color_countdown2=(0,0,0)       #倒數計時的數字2(警告時)
#倒數計時模式
# speech_model1=[3000,600,300]                   #50分鐘\10分鐘\5分鐘
# speech_model2=[600,180,120]                    #10分鐘\3分鐘\2分鐘
# speech_model3=[60,15,5]                        #60秒\15秒\5秒
# speech_model4=[300,120]

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

#打開記事本
file=open(f'TWSIAM\\schedule_day{schedule_time}.txt','r',encoding="utf-8")
schedule_today=file.readlines()
schedule_today_len=len(schedule_today)
file.close()  

#紀錄每個活動開始與結束的時間
schedule_startsec=[]
schedule_endsec=[]
for i in range(1,schedule_today_len):
    n=schedule_today[i]
    y=list(n)
    schedule_hour=y[0:2]
    schedule_hour="".join(schedule_hour)
    schedule_min=y[3:5]
    schedule_min="".join(schedule_min)
    schedule_startsec.append(int(schedule_hour)*3600+int(schedule_min)*60)

    schedule_hour=y[6:8]
    schedule_hour="".join(schedule_hour)
    schedule_min=y[9:11]
    schedule_min="".join(schedule_min)
    schedule_endsec.append(int(schedule_hour)*3600+int(schedule_min)*60)

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
            if event.type == pg.QUIT:                 #如果按叉叉就把視窗關掉
                pg.quit()
                return True
            elif event.type == pg.KEYUP:              #如果按鍵盤就進入主畫面
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
        if close:
            break
        show_init=False
    
    clock.tick(FPS)  # 一秒最多運行FPS次

    # 取得輸入
    if schedule_today_len<=1:
        draw_text(screen,"今日未設定行程",word_size+20,(WIDTH_init/2)-(word_size+20)*(3.5),HEIGHT_init/2+((word_size+20)/2),remaining_number_color_countdown1)
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
    else:
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
        zoom_mult=2
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

        #算出現在是哪個活動
        time1=time.localtime()
        now_sec=time1.tm_hour*3600+time1.tm_min*60+time1.tm_sec
        for i in range(len(schedule_startsec)):
            x=schedule_startsec[i]
            y=schedule_endsec[i]
            z=(now_sec-int(x))*(now_sec-int(y))
            if int(z)<=0:
                break
        
        speech_time=int(schedule_endsec[i]-schedule_startsec[i]) #這個活動的時間有多長
        active_now='現在議程:'+schedule_today[i+1]
        active_now=prune(active_now)

        if i<schedule_today_len-2:
            active_next='下個議程:'+schedule_today[i+2]
            active_next=prune(active_next)
        
        remaining_time_sec=int(schedule_endsec[i])-now_sec
        x=str(int(remaining_time_sec)//60)
        y=str(int(remaining_time_sec)%60)
        if len(x)==1:
            x='0'+x
        if len(y)==1:
            y='0'+y
        remaining_time=x+':'+y

        # if speech_time==speech_model1[0]:
        #     speech_remaing_time1=speech_model1[1]
        #     speech_remaing_time2=speech_model1[2]
        # elif speech_time==speech_model2[0]:
        #     speech_remaing_time1=speech_model2[1]
        #     speech_remaing_time2=speech_model2[2]
        # elif speech_time==speech_model3[0]:
        #     speech_remaing_time1=speech_model3[1]
        #     speech_remaing_time2=speech_model3[2]
        # else:
        #     speech_remaing_time1=speech_model4[0]
        #     speech_remaing_time2=speech_model4[1]
        
        #畫面顯示
        # if remaining_time_sec>speech_remaing_time1:
        #     screen.fill(backgroung_color_normal)
        #     draw_text(screen,str(remaining_time),number_size,WIDTH/2-number_size*(5/4),HEIGHT/2-number_size*(5/8),remaining_number_color_normal)   
        # elif remaining_time_sec<=speech_remaing_time1 and remaining_time_sec>speech_remaing_time2:
        #     screen.fill(backgroung_color_countdown1)
        #     draw_text(screen,str(remaining_time),number_size,WIDTH/2-number_size*(5/4),HEIGHT/2-number_size*(5/8),remaining_number_color_countdown1) 
        # else:
        #     screen.fill(backgroung_color_countdown2)
        #     draw_text(screen,str(remaining_time),number_size,WIDTH/2-number_size*(5/4),HEIGHT/2-number_size*(5/8),remaining_number_color_countdown2) 
        
        screen.fill(backgroung_color_normal)
        draw_text(screen,str(remaining_time),number_size,WIDTH/2-number_size*(5/4),HEIGHT/2-number_size*(5/8),remaining_number_color_normal)
    
        all_sprites.draw(screen)
        draw_text(screen,str(now_moment),word_size,line_space_size,line_space_size,word_color)
        draw_text(screen,str(active_now),word_size,line_space_size,line_space_size*(6/5)+word_size,word_color)
        if i<schedule_today_len-2:
            draw_text(screen,str(active_next),word_size,line_space_size,HEIGHT-line_space_size-word_size,word_color)
    pg.display.update()
pg.quit()
