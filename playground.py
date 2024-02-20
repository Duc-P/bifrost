from tkinter import *
import time
import random
from pynput import keyboard
from pynput.keyboard import Key, Controller
from PIL import ImageTk, Image

# custom volcanic colors
vc_yellow = "#F7F002"
vc_burntyellow = "#F5B91D"
vc_orange = "#F06625"
vc_red = "#950A11"
vc_plum = "#310600"

vc_darkash = "#3A3A3A"
vc_medash = "#838383"
vc_lightash = "#AEAEAE"
vc_lightestash = "#C9C9C9"

# window
window = Tk()
window.minsize(width=window.winfo_screenwidth(),height=window.winfo_screenheight())
window.config(bg=vc_plum)
window.state('zoomed')

# window settings
WIDTH = window.winfo_screenwidth()
HEIGHT = window.winfo_screenheight()

# timers (ms)
time_played = 0
time_left = 50000 # 50 seconds
dilation = 0
dilation_cap = 900
dilation_rate = 6
cooldown = 5 # in seconds

# time earned (ms)
large_catch = 30000
med_catch = 15000
small_catch = 5000

# coordinates
x_g = random.randint(round(WIDTH*0.2),round(WIDTH*0.6))
y_g = random.randint(round(HEIGHT*0.2),round(HEIGHT*0.6))
x_z = random.randint(round(WIDTH*0.2),round(WIDTH*0.65))
y_z = random.randint(round(HEIGHT*0.2),round(HEIGHT*0.65))

# velocity
vel_x_g = 7
vel_y_g = 7
vel_x_temp = 7
vel_y_temp = 7

# misc
strike = False # can toggle via settings and strike
streak = 0
icon_size = 60

# canvas and zones
canvas = Canvas(window,width=WIDTH*0.7,height=HEIGHT*0.7)
canvas.config(bg="black",borderwidth=0,highlightthickness=0)
canvas.place(x=WIDTH*0.15, y=HEIGHT*0.15)
zone_S = canvas.create_rectangle(x_z-WIDTH*0.2, y_z-HEIGHT*0.2, x_z+WIDTH*0.2, y_z+HEIGHT*0.2,
                                fill = vc_red, outline = vc_red)
zone_M = canvas.create_rectangle(x_z-WIDTH*0.125, y_z-HEIGHT*0.125, x_z+WIDTH*0.125, y_z+HEIGHT*0.125,
                                fill = vc_burntyellow, outline = vc_burntyellow)
zone_L = canvas.create_rectangle(x_z-WIDTH*0.05, y_z-HEIGHT*0.05, x_z+WIDTH*0.05, y_z+HEIGHT*0.05, 
                                fill = vc_yellow, outline = vc_yellow)

# gauge
photo_image = PhotoImage(file='fragment.png') # 60x60 pixels
my_image = canvas.create_image(x_g,y_g,image=photo_image,anchor=NW)
image_width = photo_image.width()
image_height = photo_image.height()

# update timer
def update():
    global time_left, time_played, vel_x_g, vel_y_g, dilation
    time_left -= 1000
    time_played += 1000
    lb_time_left.configure(text=round(time_left/1000))

    if time_left > 0:
        # schedule next update 1000 ms later
        window.after(1000-dilation, update)
    elif time_left <= 0:
        lb_time_left.configure(text="0")
        lb_time_left.place(x=WIDTH*0.485,y=HEIGHT*0.05)
    if 0<=time_left<=20:
        lb_time_left.config(fg=vc_red)
        lb_time_left.place(x=WIDTH*0.475,y=HEIGHT*0.05)
    elif 10 <= time_left <= 99:
        lb_time_left.place(x=WIDTH*0.45,y=HEIGHT*0.05)
    elif time_left > 99:
        lb_time_left.place(x=WIDTH*0.428,y=HEIGHT*0.05)
    if dilation <= dilation_cap:
        dilation += dilation_rate
        #print("time dilation:",dilation)
window.after(1000-dilation, update) # start the update 1 second later

# time left label
lb_time_left = Label(window, text=round(time_left/1000), font=("Courier", round(WIDTH*0.04)),borderwidth=0,highlightthickness=0)
lb_time_left.place(x=WIDTH*0.45,y=HEIGHT*0.05)
lb_time_left.config(bg= vc_plum, fg= vc_burntyellow)
lb_text_left = Label(window, text="TIME LEFT", font=("Courier", round(WIDTH*0.01)),borderwidth=0,highlightthickness=0)
lb_text_left.place(x=WIDTH*0.46,y=HEIGHT*0.02)
lb_text_left.config(bg= vc_plum, fg= vc_burntyellow)

# streak label
lb_streak = Label(window, text=streak, font=("Courier", round(WIDTH*0.04)),borderwidth=0,highlightthickness=0)
lb_streak.place(x=WIDTH*0.9,y=HEIGHT*0.5)
lb_streak.config(bg= vc_plum, fg= vc_lightestash)

class Keylistener():
    def on_press(key):
        global x_g, y_g, x_z, y_z, is_L, is_M, is_S, time_left, streak, strike 
        global large_catch, med_catch, small_catch, vel_x_g, vel_y_g, vel_x_temp, vel_y_temp
        global canvas, zone_S, zone_M, zone_L

        coordinates = canvas.coords(my_image)
        is_S = (coordinates[0]>=(x_z-WIDTH*0.2)) and (coordinates[0]+icon_size<=(x_z+WIDTH*0.2)) and (coordinates[1]>=(y_z-HEIGHT*0.2)) and (coordinates[1]+icon_size<=(y_z+HEIGHT*0.2))
        is_M = (coordinates[0]>=(x_z-WIDTH*0.125)) and (coordinates[0]+icon_size<=(x_z+WIDTH*0.125)) and (coordinates[1]>=(y_z-HEIGHT*0.125)) and (coordinates[1]+icon_size<=(y_z+HEIGHT*0.125))
        is_L = (coordinates[0]>=(x_z-WIDTH*0.05)) and (coordinates[0]+icon_size<=(x_z+WIDTH*0.05)) and (coordinates[1]>=(y_z-HEIGHT*0.05)) and (coordinates[1]+icon_size<=(y_z+HEIGHT*0.05))
        try:
            # highest score is earned when is_S and is_M and is_L is true
            if key == Key.space and is_L:
                #print("high scoring score")
                strike = True
                vel_x_temp = vel_x_g
                vel_y_temp = vel_y_g
                x_z = random.randint(round(WIDTH*0.2),round(WIDTH*0.65))
                y_z = random.randint(round(HEIGHT*0.2),round(HEIGHT*0.65))
                canvas.coords(zone_S,x_z-WIDTH*0.2, y_z-HEIGHT*0.2, x_z+WIDTH*0.2, y_z+HEIGHT*0.2)
                canvas.coords(zone_M,x_z-WIDTH*0.125, y_z-HEIGHT*0.125, x_z+WIDTH*0.125, y_z+HEIGHT*0.125)
                canvas.coords(zone_L,x_z-WIDTH*0.05, y_z-HEIGHT*0.05, x_z+WIDTH*0.05, y_z+HEIGHT*0.05)
                canvas.itemconfig(zone_S, fill=vc_darkash, outline=vc_darkash)
                canvas.itemconfig(zone_M, fill=vc_lightash, outline=vc_lightash)
                canvas.itemconfig(zone_L, fill=vc_lightestash, outline=vc_lightestash)
                time_left += large_catch
                streak += 1
                lb_streak.config(text=streak)
                if streak == 0:
                    lb_streak.config(fg=vc_lightestash)
                elif streak == 1:
                    lb_streak.config(fg=vc_orange)
                elif streak == 2:
                    lb_streak.config(fg=vc_burntyellow)
                elif streak == 3:
                    lb_streak.config(fg=vc_yellow)
                print("time gained: ",large_catch/1000)
                time.sleep(cooldown)
                strike = False
                vel_x_g = vel_x_temp
                vel_y_g = vel_y_temp
                canvas.itemconfig(zone_S, fill=vc_red, outline=vc_red)
                canvas.itemconfig(zone_M, fill=vc_burntyellow, outline=vc_burntyellow)
                canvas.itemconfig(zone_L, fill=vc_yellow, outline=vc_yellow)
            elif key == Key.space and is_M:
                #print("medium scoring zone")
                strike = True
                vel_x_temp = vel_x_g
                vel_y_temp = vel_y_g
                x_z = random.randint(round(WIDTH*0.2),round(WIDTH*0.65))
                y_z = random.randint(round(HEIGHT*0.2),round(HEIGHT*0.65))
                canvas.coords(zone_S,x_z-WIDTH*0.2, y_z-HEIGHT*0.2, x_z+WIDTH*0.2, y_z+HEIGHT*0.2)
                canvas.coords(zone_M,x_z-WIDTH*0.125, y_z-HEIGHT*0.125, x_z+WIDTH*0.125, y_z+HEIGHT*0.125)
                canvas.coords(zone_L,x_z-WIDTH*0.05, y_z-HEIGHT*0.05, x_z+WIDTH*0.05, y_z+HEIGHT*0.05)
                canvas.itemconfig(zone_S, fill=vc_darkash, outline=vc_darkash)
                canvas.itemconfig(zone_M, fill=vc_lightash, outline=vc_lightash)
                canvas.itemconfig(zone_L, fill=vc_lightestash, outline=vc_lightestash)
                time_left += med_catch
                streak += 1
                lb_streak.config(text=streak)
                if streak == 0:
                    lb_streak.config(fg=vc_lightestash)
                elif streak == 1:
                    lb_streak.config(fg=vc_orange)
                elif streak == 2:
                    lb_streak.config(fg=vc_burntyellow)
                elif streak == 3:
                    lb_streak.config(fg=vc_yellow)
                print("time gained: ",med_catch/1000)
                time.sleep(cooldown)
                strike = False
                vel_x_g = vel_x_temp
                vel_y_g = vel_y_temp
                canvas.itemconfig(zone_S, fill=vc_red, outline=vc_red)
                canvas.itemconfig(zone_M, fill=vc_burntyellow, outline=vc_burntyellow)
                canvas.itemconfig(zone_L, fill=vc_yellow, outline=vc_yellow)
            elif key == Key.space and is_S:
                #print("low scoring zone")
                strike = True
                vel_x_temp = vel_x_g
                vel_y_temp = vel_y_g
                x_z = random.randint(round(WIDTH*0.2),round(WIDTH*0.65))
                y_z = random.randint(round(HEIGHT*0.2),round(HEIGHT*0.65))
                canvas.coords(zone_S,x_z-WIDTH*0.2, y_z-HEIGHT*0.2, x_z+WIDTH*0.2, y_z+HEIGHT*0.2)
                canvas.coords(zone_M,x_z-WIDTH*0.125, y_z-HEIGHT*0.125, x_z+WIDTH*0.125, y_z+HEIGHT*0.125)
                canvas.coords(zone_L,x_z-WIDTH*0.05, y_z-HEIGHT*0.05, x_z+WIDTH*0.05, y_z+HEIGHT*0.05)
                canvas.itemconfig(zone_S, fill=vc_darkash, outline=vc_darkash)
                canvas.itemconfig(zone_M, fill=vc_lightash, outline=vc_lightash)
                canvas.itemconfig(zone_L, fill=vc_lightestash, outline=vc_lightestash)
                time_left += small_catch
                streak += 1
                lb_streak.config(text=streak)
                if streak == 0:
                    lb_streak.config(fg=vc_lightestash)
                elif streak == 1:
                    lb_streak.config(fg=vc_orange)
                elif streak == 2:
                    lb_streak.config(fg=vc_burntyellow)
                elif streak == 3:
                    lb_streak.config(fg=vc_yellow)
                print("time gained: ",small_catch/1000)
                time.sleep(cooldown)
                strike = False
                vel_x_g = vel_x_temp
                vel_y_g = vel_y_temp
                canvas.itemconfig(zone_S, fill=vc_red, outline=vc_red)
                canvas.itemconfig(zone_M, fill=vc_burntyellow, outline=vc_burntyellow)
                canvas.itemconfig(zone_L, fill=vc_yellow, outline=vc_yellow)
            else:
                #print("miss")
                strike = True
                vel_x_temp = vel_x_g
                vel_y_temp = vel_y_g
                x_z = random.randint(round(WIDTH*0.2),round(WIDTH*0.65))
                y_z = random.randint(round(HEIGHT*0.2),round(HEIGHT*0.65))
                canvas.coords(zone_S,x_z-WIDTH*0.2, y_z-HEIGHT*0.2, x_z+WIDTH*0.2, y_z+HEIGHT*0.2)
                canvas.coords(zone_M,x_z-WIDTH*0.125, y_z-HEIGHT*0.125, x_z+WIDTH*0.125, y_z+HEIGHT*0.125)
                canvas.coords(zone_L,x_z-WIDTH*0.05, y_z-HEIGHT*0.05, x_z+WIDTH*0.05, y_z+HEIGHT*0.05)
                canvas.itemconfig(zone_S, fill=vc_darkash, outline=vc_darkash)
                canvas.itemconfig(zone_M, fill=vc_lightash, outline=vc_lightash)
                canvas.itemconfig(zone_L, fill=vc_lightestash, outline=vc_lightestash)
                streak = 0
                lb_streak.config(text=streak)
                if streak == 0:
                    lb_streak.config(fg=vc_lightestash)
                elif streak == 1:
                    lb_streak.config(fg=vc_orange)
                elif streak == 2:
                    lb_streak.config(fg=vc_burntyellow)
                elif streak == 3:
                    lb_streak.config(fg=vc_yellow)
                print("time gained: 0")
                time.sleep(cooldown)
                strike = False
                vel_x_g = vel_x_temp
                vel_y_g = vel_y_temp
                canvas.itemconfig(zone_S, fill=vc_red, outline=vc_red)
                canvas.itemconfig(zone_M, fill=vc_burntyellow, outline=vc_burntyellow)
                canvas.itemconfig(zone_L, fill=vc_yellow, outline=vc_yellow)
            print("<<<===>>>")
            if 1 <= streak <= 3:
                large_catch = 30000 + large_catch*0.3*streak
                med_catch = 15000 +  med_catch*0.2*streak
                small_catch = 5000 + small_catch*0.1*streak
            elif streak == 0:
                large_catch = 30000
                med_catch = 15000
                small_catch = 5000

        except AttributeError:
            #print('special key {0} pressed'.format(key))
            print("something went wrong?")
    def on_release(key):
      if key == keyboard.Key.esc:
         # stop listener
         return False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def animate_gauge():
    global x_g, y_g, my_image, vel_x_g, vel_y_g, vel_x_temp, vel_y_temp, is_S, is_M, is_L, strike

    coordinates = canvas.coords(my_image)
    #print(coordinates)
    if (coordinates[0]>=(WIDTH*0.7-image_width) or coordinates[0]<0):
        vel_x_g = -vel_x_g
    if (coordinates[1]>=(HEIGHT*0.7-image_height) or coordinates[1]<0):
        vel_y_g = -vel_y_g
    if strike == True:
        vel_x_g = 0
        vel_y_g = 0
    canvas.move(my_image,vel_x_g,vel_y_g)
    # refresh rate: 10 ms 
    canvas.after(10, animate_gauge)
    #window.update()

animate_gauge()

window.mainloop()