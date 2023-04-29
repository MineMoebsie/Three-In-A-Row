import pygame as pg
import numpy as np
import time as t
import random as r
import pdb

pg.init()
pg.font.init()


#screen = pg.display.set_mode((600,600),pg.SCALED|pg.DOUBLEBUF|pg.HWSURFACE)#surface for the game only
screen = pg.Surface((600,600),pg.DOUBLEBUF|pg.HWSURFACE)
screenblit = pg.display.set_mode((1600,900),pg.RESIZABLE|pg.DOUBLEBUF|pg.HWSURFACE)#actual surface, resizable etc.

pg.scrap.init()

screen_xy = screen.get_width() #width and height are same (square)

f = open("scores.txt")
stats_dict = eval(f.read())
f.close()

logo_dark = pg.image.load("logo_dark.png").convert_alpha()
pg.display.set_caption("Three In A Row","3 in a row")
pg.display.set_icon(logo_dark)
desktop_sizes = pg.display.get_desktop_sizes()
desktop_size = desktop_sizes[0]
screen_width = desktop_size[0]
screen_height = desktop_size[1]
playing = True

sound = True #if sound is false, no sound.
win_sound = pg.mixer.Sound("win.wav")
complete_sound = pg.mixer.Sound("complete.wav")
tick_sound = pg.mixer.Sound("tick.wav")
draw_sound = pg.mixer.Sound("draw.wav")

decline_music = pg.mixer.Sound("decline.wav")

chnl_sfx = pg.mixer.Channel(1)
chnl_sfx.set_volume(0.1)

chnl_music = pg.mixer.Channel(2)
chnl_music.set_volume(0.1)

played_complete_sound = False

#functions and classes
def draw_grid(screen, grid, grid_size, win_grid, expand_animation, screen_xy):#, line_picture_vert=line_picture_vert,line_picture_horiz=line_picture_horiz):
    grid_square = round(screen_xy/grid_size)
    win1_color = (97, 19, 9)
    win2_color = (23, 37, 115)
    win3_color = (20, 84, 47)
    win4_color = (74, 16, 57)
    num_to_char_dict = {1:"x",2:"o",3:"r",4:"d"}
    if grid_size >= 11:
        line_picture_vert_ = line_thin_picture_vert
        line_picture_horiz_ = line_thin_picture_horiz
    else:
        line_picture_vert_ = line_picture_vert
        line_picture_horiz_ = line_picture_horiz

    if expand_animation == 0:    
        for x in range(grid_size):
            for y in range(grid_size):
                if win_grid[y,x] > 0:
                    pg.draw.rect(screen,eval("win"+str(int(win_grid[y,x]))+"_color"),((x*grid_square, y*grid_square),(grid_square, grid_square)))
                    
                if grid[y, x] > 0:
                    screen.blit(eval(num_to_char_dict[int(grid[y,x])]+"_picture"),(x*grid_square, y*grid_square))

        middle_dist = grid_square
        midxy = round(screen_xy/2) #midpoint of screen
        for line in range(int((grid_size)/2-0.5)):
            screen.blit(line_picture_horiz_,(0,midxy-(middle_dist/2)-(middle_dist*line)-5))
            screen.blit(line_picture_vert_,(midxy-(middle_dist/2)-(middle_dist*line)-5,0))

            screen.blit(line_picture_horiz_,(0,midxy+(middle_dist/2)+(middle_dist*line)-5))
            screen.blit(line_picture_vert_,(midxy+(middle_dist/2)+(middle_dist*line)-5,0))
                
                    
    else:#line animation: fade out
        if expand_animation < 0.25:
            i = (-expand_animation * 1020) + 255
            x_pic_alpha = x_picture
            o_pic_alpha = o_picture
            r_pic_alpha = r_picture
            d_pic_alpha = d_picture

            x_pic_alpha.set_alpha(i)
            o_pic_alpha.set_alpha(i)
            r_pic_alpha.set_alpha(i)
            d_pic_alpha.set_alpha(i)

            x_win = pg.Surface((grid_square, grid_square))
            o_win = pg.Surface((grid_square, grid_square))
            r_win = pg.Surface((grid_square, grid_square))
            d_win = pg.Surface((grid_square, grid_square))

            x_win.set_alpha(i)
            o_win.set_alpha(i)
            r_win.set_alpha(1)
            d_win.set_alpha(1)

            x_win.fill(win1_color)
            o_win.fill(win2_color)
            r_win.fill(win3_color)
            d_win.fill(win4_color)

            for x in range(grid_size):
                for y in range(grid_size):
                    if win_grid[y, x] > 0:
                        screen.blit(eval(num_to_char_dict[int(win_grid[y,x])]+"_win"),(x*grid_square,y*grid_square))

                    if grid[y, x] > 0:
                        screen.blit(eval(num_to_char_dict[int(grid[y,x])]+"_pic_alpha"),(x*grid_square,y*grid_square))
                        
            middle_dist = grid_square
            midxy = round(screen_xy/2) #midpoint of screen
            for line in range(int((grid_size)/2-0.5)):
                screen.blit(line_picture_horiz_,(0,midxy-(middle_dist/2)-(middle_dist*line)-5))
                screen.blit(line_picture_vert_,(midxy-(middle_dist/2)-(middle_dist*line)-5,0))

                screen.blit(line_picture_horiz_,(0,midxy+(middle_dist/2)+(middle_dist*line)-5))
                screen.blit(line_picture_vert_,(midxy+(middle_dist/2)+(middle_dist*line)-5,0))

            
            
        elif expand_animation < 0.751: #line animation
            new_grid_square = screen_xy/grid_size
            grid_size -= 2
            grid_square = screen_xy/grid_size
            middle_dist = round((expand_animation-0.25)*((-grid_square+new_grid_square)/0.5) + grid_square)
            midxy = round(screen_xy/2) #midpoint of screen
            for line in range(int(grid_size/2-0.5)):
                screen.blit(line_picture_horiz_,(0,midxy-(middle_dist/2)-(middle_dist*line)-5))
                screen.blit(line_picture_vert_,(midxy-(middle_dist/2)-(middle_dist*line)-5,0))

                screen.blit(line_picture_horiz_,(0,midxy+(middle_dist/2)+(middle_dist*line-5)))
                screen.blit(line_picture_vert_,(midxy+(middle_dist/2)+(middle_dist*line)-5,0))
                
        else: #fade in stuff
            i = (expand_animation * 1020) - 765

            x_pic_alpha = x_picture
            o_pic_alpha = o_picture
            r_pic_alpha = r_picture
            d_pic_alpha = d_picture

            x_pic_alpha.set_alpha(i)
            o_pic_alpha.set_alpha(i)
            r_pic_alpha.set_alpha(i)
            d_pic_alpha.set_alpha(i)

            x_win = pg.Surface((grid_square, grid_square))
            o_win = pg.Surface((grid_square, grid_square))
            r_win = pg.Surface((grid_square, grid_square))
            d_win = pg.Surface((grid_square, grid_square))

            x_win.set_alpha(i)
            o_win.set_alpha(i)
            r_win.set_alpha(i)
            d_win.set_alpha(i)

            x_win.fill(win1_color)
            o_win.fill(win2_color)
            r_win.fill(win3_color)
            d_win.fill(win4_color)

            line_picture_vert_.set_alpha(255)
            line_picture_horiz_.set_alpha(255)
            
            for x in range(grid_size):
                for y in range(grid_size):
                    if win_grid[y, x] > 0:
                        screen.blit(eval(num_to_char_dict[int(win_grid[y,x])]+"_win"),(x*grid_square,y*grid_square))

                    if grid[y, x] > 0:
                        screen.blit(eval(num_to_char_dict[int(grid[y,x])]+"_pic_alpha"),(x*grid_square,y*grid_square))

                    
                        
            middle_dist = grid_square
            midxy = round(screen_xy/2) #midpoint of screen
            for line in range(int((grid_size-2)/2-0.5)):
                screen.blit(line_picture_horiz_,(0,midxy-(middle_dist/2)-(middle_dist*line)-5))
                screen.blit(line_picture_vert_,(midxy-(middle_dist/2)-(middle_dist*line)-5,0))

                screen.blit(line_picture_horiz_,(0,midxy+(middle_dist/2)+(middle_dist*line)-5))
                screen.blit(line_picture_vert_,(midxy+(middle_dist/2)+(middle_dist*line)-5,0))
            
            
            line_picture_vert.set_alpha(i)
            line_picture_horiz.set_alpha(i)
            line += 1
            screen.blit(line_picture_horiz_,(0,midxy-(middle_dist/2)-(middle_dist*line)-5))
            screen.blit(line_picture_vert_,(midxy-(middle_dist/2)-(middle_dist*line)-5,0))

            screen.blit(line_picture_horiz_,(0,midxy+(middle_dist/2)+(middle_dist*line)-5))
            screen.blit(line_picture_vert_,(midxy+(middle_dist/2)+(middle_dist*line)-5,0))

def convert_grid(grid,spawned_p_win_grid,grid_size):
    new_gr_size = grid_size + 2
    new_grid = np.zeros((new_gr_size,new_gr_size))
    new_grid[1:-1, 1:-1] = np.copy(grid[:,:])
    grid = new_grid

    new_gr_size = grid_size + 2
    new_grid = np.zeros((new_gr_size,new_gr_size))
    new_grid[1:-1, 1:-1] = np.copy(spawned_p_win_grid[:,:])
    spawned_p_win_grid = new_grid
    return grid, spawned_p_win_grid, new_gr_size

def calculate_mouse_pos(mx, my, grid_size, screen_xy, blit_x, blit_y):
    grid_square = screen_xy/grid_size
    mrx = 0
    mry = 0
    mx -= blit_x
    my -= blit_y
    mrx = int(mx/grid_square)
    mry = int(my/grid_square)
    return mrx, mry

def calculate_if_row(grid, grid_size, win_grid,tiles_covered,p_win_grid,end_of_game=False):
    win = 0 #if win 1: x has won, if win 2: o has won etc.
    grid_win_line = []
    line_width = 10
    half_l_w = int(line_width/2)
    grid_square = int(600/grid_size)
    half_gr_s = int(600/grid_size/2)
    
    #check horizontally
    for y in range(grid_size):
        for x in range(grid_size-2):
            if grid[y,x] == grid[y,x+1] and grid[y,x+1] == grid[y,x+2] and grid[y,x] != 0:
                #horizontal win
                for x_win in range(3):
                    win_grid[y,x+x_win] = grid[y,x]
                    p_win_grid[y,x+x_win] = grid[y,x]

    #check vertically
    for x in range(grid_size):
        for y in range(grid_size-2):
            if grid[y,x] == grid[y+1,x] and grid[y+1,x] == grid[y+2,x] and grid[y,x] != 0:
                #vertical win
                for y_win in range(3):
                    win_grid[y+y_win,x] = grid[y,x]
                    p_win_grid[y+y_win,x] = grid[y,x]

    #check diagonally
    for move_x in range(grid_size-2):
        for move_y in range(grid_size-2):
            if grid[move_y + 1, move_x + 1]:
                player_type = grid[move_y + 1, move_x + 1]
                if grid[move_y, move_x] == grid[move_y+2,move_x+2] and grid[move_y, move_x] == player_type:
                    #diagonal win
                    for win_ in range(3):
                        win_grid[move_y+win_, move_x+win_] = player_type
                        p_win_grid[move_y+win_, move_x+win_] = player_type
                if grid[move_y+2, move_x] == grid[move_y,move_x+2] and grid[move_y+2, move_x] == player_type:
                    #diagonal win
                    for win_ in range(3):
                        win_grid[move_y+(-win_+2), move_x+win_] = player_type
                        p_win_grid[move_y+(-win_+2), move_x+win_] = player_type
    
    num_to_char_dict = {1:"x",2:"o",3:"r",4:"d"}
    win_scores = {1:0,2:0,3:0,4:0}

    for x in range(1,5):
        win_scores[x] = np.count_nonzero(win_grid == x)

    for x in range(1,5):
        if win_scores[x] >= tiles_covered and tiles_covered != 0:
            win = num_to_char_dict[x]
            break
    
    if end_of_game and win == 0: #grid expanded max amount of times and no winner yet
        win_index = max(win_scores, key=win_scores.get)
        win_index_full = num_to_char_dict[win_index]
        if win_scores[win_index] > 0:
            for x in range(1,5):
                if win_scores[x] == win_scores[win_index] and x != win_index:
                    win_index_full = str(win_index_full)+str(num_to_char_dict[x])
            win = win_index_full
    
    if end_of_game: #write to stats_dict
        for x in range(1,5):
            stats_dict['area_covered'][x-1] += win_scores[x]

    return win, grid_win_line, win_grid,win_scores,p_win_grid

def screen_calc(win_w,win_h):
    largest_win_size = min(win_w,win_h)
    if largest_win_size > 250:
        largest_win_size -= 50
    return largest_win_size

def reload_img(screen_xy,grid_size):
    line_picture_vert = pg.image.load("line.png").convert_alpha()
    line_picture_vert = pg.transform.scale(line_picture_vert,(10,screen_xy))
    line_picture_horiz = pg.transform.rotate(line_picture_vert, 90)

    line_thin_picture_vert = pg.image.load("line_thin.png").convert_alpha()
    line_thin_picture_vert = pg.transform.scale(line_thin_picture_vert,(10,screen_xy))
    line_thin_picture_horiz = pg.transform.rotate(line_thin_picture_vert, 90)

    x_picture = pg.image.load("x.png").convert_alpha()
    o_picture = pg.image.load("o.png").convert_alpha()
    r_picture = pg.image.load("r.png").convert_alpha()
    d_picture = pg.image.load("d.png").convert_alpha()
    x_picture = pg.transform.scale(x_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
    o_picture = pg.transform.scale(o_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
    r_picture = pg.transform.scale(r_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
    d_picture = pg.transform.scale(d_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))

def draw_menu(screenblit, menu_type, fonts,btn_list,slider_list,grid_expansions,player_count,tiles_covered,title_h,stats_view,stats_dict,reset_confirmed,copied,sound):
    arr_rect_r = pg.Rect((-100,-100),(0,0))
    arr_rect_l = pg.Rect((-100,-100),(0,0))

    screen_w, screen_h = screenblit.get_size()
    btn_w = round(screen_w / 5)
    btn_h = round(btn_w / 2)
    subtitle_spacing = 1.8

    num_to_char_dict = {1:"x",2:"o",3:"r",4:"d"}
            
    if menu_type == "main": #main menu (when you launch the game)
        title_w, title_h = set_text(fonts, "Three in a row", 10,10, "main_font", screenblit,align="x")

    elif menu_type == "play":
        title_w, title_h = set_text(fonts, "Start game", 0,10, "main_font", screenblit,align="x")
        subt_w, subt_h = set_text(fonts, "Map expansions:" + " " * 40, 0,(title_h*subtitle_spacing-title_h)*(1+0.25) + 10, "btn_font", screenblit,align="x")
        subt_w, subt_h = set_text(fonts, "Players:" + " " * 40, 0,(title_h*subtitle_spacing-title_h)*(2+0.25) + 10, "btn_font", screenblit,align="x")
        subt_w, subt_h = set_text(fonts, "Area needed to win:" + " " * 40, 0,(title_h*subtitle_spacing-title_h)*(3+0.25) + 10, "btn_font", screenblit,align="x")
        set_text(fonts, "Press S to toggle sound", 0,(title_h*subtitle_spacing-title_h)*(4.15) + 10, "about_font", screenblit,align="x")
        if not sound:
            blit_x,blit_y = rel_coords(0,850,screenblit)
            set_text(fonts,"Sound muted",0,blit_y,"btn_font",screenblit,align="x")
            

    elif menu_type == "about":
        title_w, title_h = set_text(fonts, "About", 0,10, "main_font", screenblit,align="x")
        text_w, text_h = fonts["about_font"].size("Test")
        text_h = text_h * 1.1
        set_text(fonts,'''I created "Three In A Row" as my first complete polished game. I kept''',     0,title_h,"about_font",screenblit,align="x")
        set_text(fonts,'''it simple so that I could get more experience with game design:''',           0,title_h + 1*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''creating a friendly user interface, making clear when a player''',            0,title_h + 2*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''has won or has covered more area on the board, adding a stats menu ''',       0,title_h + 3*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''that is clear to navigate, adding sound effects, etc.''',                     0,title_h + 4*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''Thank you for playing! I hope that you enjoyed it.''',                        0,title_h + 5*text_h,"about_font",screenblit,align="x")
        set_text(fonts,''' ''',                                                                         0,title_h + 6*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''Credits (source: freesound.org): ''',                                         0,title_h + 7*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''file in folder (used...) -> Artist - Title''',                      0,title_h + 8*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''complete.wav (played at end of game: win) -> Unlistenable - "Electro Win Sound"''',0,title_h + 9*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''decline.wav (ambient background music) -> Andrewkn - "Decline"''',            0,title_h + 10*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''draw.wav (played at end of game: draw) -> Annyew - "Complete/obtained sound"''',0,title_h + 11*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''tick.wav (played when someone clicks) -> NenadSimic - "Button Tick"''',       0,title_h + 12*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''win.wav (played at covering area) -> Jerimee - "Objective Complete"''',       0,title_h + 13*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''Roboto-Regular.ttf (font) -> Google Fonts''',                                 0,title_h + 14*text_h,"about_font",screenblit,align="x")
        set_text(fonts,'''Feedback is very much appreciated! Join my Discord server: (press C to copy to clipboard).''',               0,title_h + 15*text_h,"about_font",screenblit,align="x")

        if copied:
            blit_x,blit_y = rel_coords(0,850,screenblit)
            set_text(fonts,"Link copied to clipboard",0,blit_y,"btn_font",screenblit,align="x")

    elif menu_type == "stats":
        title_w, title_h = set_text(fonts, "Statistics", 0,10, "main_font", screenblit,align="x")

        if stats_view == 0:
            menu_icon = logo
            blitimg_x, blitimg_y = rel_coords(0,142.5,screenblit)
        elif stats_view > 0 and stats_view <= 4:
            menu_icon = eval(num_to_char_dict[stats_view]+"_stats_picture")
            blitimg_x, blitimg_y = rel_coords(0,120,screenblit) #blitimgx not used

        blitimg_x = calc_center(screen_w,screen_h,menu_icon.get_width(),menu_icon.get_height(),get_x=True,get_y=False)
        screenblit.blit(menu_icon,(blitimg_x,blitimg_y))
        #pg.draw.line(screenblit,(200,200,200),(blitimg_x,blitimg_y),(blitimg_x+menu_icon.get_width(),blitimg_y+menu_icon.get_height()),width=4)
        #pg.draw.line(screenblit,(255,255,255),(blitimg_x,title_h*1.15),(blitimg_x+menu_icon.get_width(),title_h+menu_icon.get_height()))
        if stats_view == 0:
            subt_w, subt_h = set_text(fonts, "Map expansions: " + str(stats_dict['total_map_expansions']), 0,(title_h*subtitle_spacing-title_h)*(2.5+0.25) + 10, "btn_font", screenblit,align="x")
            subt_w, subt_h = set_text(fonts, "Games played: " + str(stats_dict['games_played']), 0,(title_h*subtitle_spacing-title_h)*(3.3+0.25) + 10, "btn_font", screenblit,align="x")
        else:
            spacing = 0.425
            start_val = 2.3
            subt_w, subt_h = set_text(fonts, "Games won: " + str(stats_dict['games_won'][stats_view-1]), 0,(title_h*subtitle_spacing-title_h)*(start_val + spacing*0) + 10, "stats_font", screenblit,align="x")
            subt_w, subt_h = set_text(fonts, "Games lost: " + str(stats_dict['games_lost'][stats_view-1]), 0,(title_h*subtitle_spacing-title_h)*(start_val + spacing*1) + 10, "stats_font", screenblit,align="x")
            subt_w, subt_h = set_text(fonts, "Games tied: " + str(stats_dict['games_tied'][stats_view-1]), 0,(title_h*subtitle_spacing-title_h)*(start_val + spacing*2) + 10, "stats_font", screenblit,align="x")
            subt_w, subt_h = set_text(fonts, "Blocks placed: " + str(stats_dict['blocks_placed'][stats_view-1]), 0,(title_h*subtitle_spacing-title_h)*(start_val + spacing*3) + 10, "stats_font", screenblit,align="x")
            subt_w, subt_h = set_text(fonts, "Area covered: " + str(stats_dict['area_covered'][stats_view-1]), 0,(title_h*subtitle_spacing-title_h)*(start_val + spacing*4) + 10, "stats_font", screenblit,align="x")  
        
        menu_icon_w, menu_icon_h = menu_icon.get_size()

        if stats_view > 0:
            if arr_r_hover:
                blit_pic = arrow_h_pic_r
            else:
                blit_pic = arrow_pic_r
            screenblit.blit(blit_pic,(blitimg_x-menu_icon_w*1.1,blitimg_y+menu_icon_h*0.2))
            arr_rect_r = pg.Rect((blitimg_x-menu_icon_w*1.1,blitimg_y+menu_icon_h*0.2),blit_pic.get_size())

        if stats_view < 4:
            if arr_l_hover:
                blit_pic = arrow_h_pic_l
            else:
                blit_pic = arrow_pic_l
            screenblit.blit(blit_pic,(blitimg_x+menu_icon_w*1.47,blitimg_y+menu_icon_h*0.2))
            arr_rect_l = pg.Rect((blitimg_x+menu_icon_w*1.47,blitimg_y+menu_icon_h*0.2),blit_pic.get_size())

        if reset_confirmed:
            blit_x,blit_y = rel_coords(0,850,screenblit)
            set_text(fonts,"Click 'Reset' again to confirm",0,blit_y,"btn_font",screenblit,align="x")

    #draw buttons
    btn_dist_y = btn_h + 25
    btn_dist_start = title_h
    for i, btn in enumerate(btn_list):
        z = btn[6]
        blit_x = calc_center(screen_w,screen_h,width=btn_w,height=btn_h,get_x=True,get_y=False)
        draw_button(screenblit,blit_x,btn_dist_start+btn_dist_y*z,btn_w,btn_h,btn[4],fonts,hover=btn_list[i][5])
        btn_list[i] = [blit_x,btn_dist_start+btn_dist_y*z,btn_w,btn_h,btn_list[i][4],btn_list[i][5],btn_list[i][6]]

    for i, slider in enumerate(slider_list):
        blit_x,blit_y = rel_coords(slider[0],slider[1],screenblit)
        draw_slider(screenblit,blit_x,blit_y,round(max(screen_w/5,100)),subt_h,slider_list[i][4])
        slider_list[i] = [slider_list[i][0],slider_list[i][1],round(max(screen_w/5,100)),subt_h,slider_list[i][4]]

        add_blit_x = 400 * (screen_w/1600)
        if i == 0: #grid expansions
            set_text(fonts,str(grid_expansions),blit_x + add_blit_x,blit_y,"btn_font",screenblit)
        elif i == 1:
            set_text(fonts,str(player_count),blit_x + add_blit_x,blit_y,"btn_font",screenblit)
        elif i == 2:
            if tiles_covered != 0:
                set_text(fonts,str(tiles_covered),blit_x + add_blit_x,blit_y,"btn_font",screenblit)
            else: #play until map completely filled
                set_text(fonts,"Map filled",blit_x + add_blit_x,blit_y,"btn_font",screenblit)

    
    return btn_list, slider_list, title_h, arr_rect_r,arr_rect_l

def draw_slider(screenblit,x,y,width,height,percentage,hover=False):
    rect = ((x,y),(width, height))
    rect_inner = ((round(x+height/4),round(y+height/4)),(round(width-height/2),round(height/2)))
    border_rad = round(height/2)
    width_line = height/2

    pg.draw.rect(screenblit,(148, 148, 148),rect, border_radius=border_rad)
    pg.draw.rect(screenblit,(187, 187, 187),rect_inner, border_radius=border_rad)

    pg.draw.circle(screenblit,(190,190,190),(round(x+width/100*percentage),round(y+height/2)),round(height/1.33))
    pg.draw.circle(screenblit,(210,210,210),(round(x+width/100*percentage),round(y+height/2)),round(height/1.33),width=round(width_line/4))

def rel_coords(x,y,screenblit):
    #origional surface is width: 1600 height: 900
    w,h = screenblit.get_size()
    x = x * (w/1600)
    y = y * (w/1600)
    return round(x),round(y)

def append_buttons(btn_list,menu_type):
    #x,y,width,height,text,hover, btn place
    if menu_type == "main": #main menu (when you launch the game)
        btn_list = [[0,0,0,0,"Play",False,0],[0,0,0,0,"Stats",False,1],[0,0,0,0,"About",False,2],[0,0,0,0,"Exit",False,3]]

    elif menu_type == "play":
        btn_list = [[0,0,0,0,"Start",False,3],[0,0,0,0,"Back",False,2]]

    elif menu_type == "stats":
        btn_list = [[0,0,0,0,"Back",False,2],[0,0,0,0,"Reset",False,3]]
    
    elif menu_type == "about":
        btn_list = [[0,0,0,0,"Back",False,3]]
    
    return btn_list

def append_sliders(slider_list,menu_type,slider_percentages):
    #x (rel),y (rel),width,height,percentage slide
    if menu_type == "main":
        slider_list = []
    elif menu_type == "play":
        slider_list = [[850,150,0,0,slider_percentages[0]],[850,260,0,0,slider_percentages[1]],[850,370,0,0,slider_percentages[2]]]
    elif menu_type == "settings":
        slider_list = []
    return slider_list

def draw_button(screenblit,x,y,width,height,text,fonts,hover=False):
    rect = ((x,y),(width, height))
    border_rad = round(height / 3.5)
    width_line = round(width/17)
    if hover:
        pg.draw.rect(screenblit,(148, 148, 148),rect, border_radius=border_rad) 
    else:
        pg.draw.rect(screenblit,(98, 98, 98),rect, border_radius=border_rad)
    text_y = round(y + (height/2) - (screenblit.get_width() / 56)) - 10 # 28  * 2 = 56
    
    set_text(fonts, text, x, text_y, "btn_font",screenblit,align="x")
    pg.draw.rect(screenblit,(255,255,255),rect,width=width_line, border_radius=border_rad)

    
def calc_center(screen_w, screen_h, width=0, height=0, get_x=False, get_y=False):
    if get_x:
        return round((screen_w - width) / 2)
    elif get_y:
        return round((screen_h - height) / 2)

def set_text(fonts, string, coordx, coordy, fonttype, screenblit, align="no align",color=(255,255,255)): #Function to set text
    font = fonts[fonttype]
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, color) 
    textRect = text.get_rect()
    w = textRect.width
    h = textRect.height
    scr_w, scr_h = screenblit.get_size()
    if align == "x":
        coordx = calc_center(scr_w, scr_h, w, h, get_x=True)
    elif align == "y":
        coordy = calc_center(scr_w, scr_h, w, h, get_y=True)
    
    screenblit.blit(text,(coordx,coordy))

    return w,h

def calc_slider_values(slider_list,grid_expansions,player_count,tiles_covered):
    #0 is map expansions (grid change)
    if not slider_list == []:
        grid_expansions = round(slider_list[0][4] / (100/7)) # 0 - 7 range (for no expansions: 0)
        player_count = round(slider_list[1][4] / (100/2) + 2) # 2 - 4 range
        grid_size_with_expansions = grid_expansions * 2 + 3
        max_tiles_covered = int((grid_size_with_expansions**2)/player_count)-3
        max_tiles_covered = max(1,max_tiles_covered) #prevent ZeroDivisionError
        tiles_covered = round(slider_list[2][4] / (100/max_tiles_covered) + 3) # 3 - (grid_expansions^2/player_count) range, 0 = most tiles covered
        if slider_list[2][4] > 97:
            tiles_covered = 0
    return grid_expansions, player_count,tiles_covered

def draw_turn(screenblit, turn, turn_animation, turn_ani_perf, player_count):
    num_to_char_dict = {1:"x",2:"o",3:"r",4:"d"}
    
    if turn_animation > 0 and t.perf_counter() + 0.01 > turn_ani_perf:
        turn_animation -= 0.02
        turn_ani_perf = t.perf_counter()
        i = round(1020*((turn_animation-0.5)**2))
        turn_dict = {1:4,2:1,3:2,4:3}
        if turn_animation >= 0.5:
            if turn == 1:
                turn_picture = eval(num_to_char_dict[player_count]+"_turn_picture")
            else:
                turn_picture = eval(num_to_char_dict[turn-1]+"_turn_picture")
        else:
            turn_picture = eval(num_to_char_dict[turn]+"_turn_picture")
        turn_picture.set_alpha(i)

    else:
        turn_picture = eval(num_to_char_dict[turn]+"_turn_picture")
    t_pic_w = turn_picture.get_width()
    x_blit,y_blit = rel_coords(10,10,screenblit)
    pg.draw.rect(screenblit,(40,40,40),((0,0),(x_blit+t_pic_w,y_blit+t_pic_w)))

    screenblit.blit(turn_picture, (x_blit,y_blit))

    return turn_animation,turn_ani_perf

def draw_end_game(screenblit, fonts, win, end_game_animation, pause_win_animation_perf):
    screen_w, screen_h = screenblit.get_size()
    font = fonts["main_font"]

    rect_i = max(min(-(150/0.3)*end_game_animation+(150/0.3), 150),0)
    #print(rect_i,end_game_animation)
    end_game_rect.set_alpha(round(rect_i))

    screen_xy = end_game_rect.get_width()

    blit_x = int((screen_w-screen_xy) / 2)
    blit_y = int((screen_h-screen_xy) / 2)

    screenblit.blit(end_game_rect, (blit_x,blit_y))


    font_colour = (210,210,210)
    if win == 0: #draw
        win_players = list(str(win))
        if len(win_players) == 1: #draw: no one won
            text_w, text_h = font.size("Draw: no one won") 

    elif len(str(win)) > 1: #draw between players
        text_w, text_h = font.size("Draw between:")

        win_pic = draw_picture
        win_pic_w, win_pic_h = win_pic.get_size()
            
    else: #player win
        text_w, text_h = font.size("has won!") 

        win_pic = win_picture
        win_pic_w, win_pic_h = win_pic.get_size()

    #textRect = text.get_rect()
    #text_w = textRect.width
    #text_h = textRect.height

    pause_time = 2

    div_num = 5 #y=x^{2}\cdot35
    #x=\frac{\sqrt{\left(y\right)}}{5.9160797831}
    div_num = np.sqrt(screen_w)/5.9160797831
    if win == 0: #draw
        if len(win_players) == 1: #draw: no one won
            blit_x = round((screen_w - text_w) / 2)
            h = round((screen_h - text_h) / 2)
            blit_y = (end_game_animation-0.5)**2 * (screen_h+text_h-h) * 4 + h

            if abs(pause_win_animation_perf) == 1:
                end_game_animation -= 0.006
            elif t.perf_counter() - pause_time > pause_win_animation_perf:
                pause_win_animation_perf = 1

            text_w, text_h = set_text(fonts, "Draw: no one won", blit_x, blit_y ,"main_font",screenblit,color=font_colour)            

    elif len(str(win)) > 1: #draw between players
        blit_x = round((screen_w - text_w - win_pic_w) / 2)
        h = round((screen_h - text_h) / 2)
        blit_y = (end_game_animation-0.5)**2 * (screen_h+text_h-h) * 4 + h

        if abs(pause_win_animation_perf) == 1:
            end_game_animation -= 0.006
        elif t.perf_counter() - pause_time > pause_win_animation_perf:
            pause_win_animation_perf = 1
            
        text_w, text_h = set_text(fonts, "Draw between", blit_x, blit_y ,"main_font",screenblit,color=font_colour)

        pic_x_blit = blit_x + text_w
        pic_y_blit = blit_y - (win_pic_h/div_num)
        screenblit.blit(win_pic,(pic_x_blit,pic_y_blit))

    else: #player win
        blit_x = round((screen_w - text_w + win_pic_w) / 2)
        h = round((screen_h - text_h) / 2)
        blit_y = (end_game_animation-0.5)**2 * (screen_h+text_h-h) * 4 + h

        if abs(pause_win_animation_perf) == 1:
            end_game_animation -= 0.006
        elif t.perf_counter() - pause_time > pause_win_animation_perf:
            pause_win_animation_perf = 1
        
        text_w, text_h = set_text(fonts, "has won!", blit_x, blit_y ,"main_font",screenblit,color=font_colour)

        pic_x_blit = blit_x - win_pic_w
        pic_y_blit = blit_y - (win_pic_h/div_num)
        screenblit.blit(win_pic,(pic_x_blit,pic_y_blit))

    if end_game_animation < 0.5 and pause_win_animation_perf == -1:
        pause_win_animation_perf = t.perf_counter()
    
    return end_game_animation,pause_win_animation_perf

def draw_particles(screenblit,particles_list):
    for particle in particles_list:
        pg.draw.rect(screenblit,particle[2],(((round(particle[0]),round(particle[1])),(round(particle[3]),round(particle[3])))))

def append_particle(particles_list, x, y, p_type,pic_size):
    #p_colors = {1:(97, 19, 9),2:(23, 37, 115),3:(20, 84, 47),4:(74, 16, 57)}
    p_colors = {1:(138, 32, 18),2:(35, 54, 158),3:(34, 156, 85),4:(128, 29, 99)}
    p_color = p_colors[p_type]
    spacing = 10
    start_size_range_min = 3
    start_size_range_max = 20
    for x_spawn in range(int(pic_size/spacing)):
        if r.randint(1,2) == 1:
            vx = r.randint(1,2)
            vy = r.randint(-4,-1)
            start_size = r.randint(start_size_range_min,start_size_range_max)
            particles_list.append([x+x_spawn*spacing,y,p_color, start_size,vx,vy])
        if r.randint(1,2) == 1:
            vx = r.randint(1,2)
            vy = r.randint(1,4)
            start_size = r.randint(start_size_range_min,start_size_range_max)
            particles_list.append([x+x_spawn*spacing,y+pic_size,p_color, start_size,vx,vy])
    
    for y_spawn in range(int(pic_size/spacing)):
        if r.randint(1,2) == 1:
            vx = r.randint(-4,-1)
            vy = r.randint(1,2)
            start_size = r.randint(start_size_range_min,start_size_range_max)
            particles_list.append([x,y+y_spawn*spacing,p_color, start_size,vx,vy])
        if r.randint(1,2) == 1:
            vx = r.randint(1,4)
            vy = r.randint(1,2)
            start_size = r.randint(start_size_range_min,start_size_range_max)
            particles_list.append([x+pic_size,y+y_spawn*spacing,p_color, start_size,vx,vy])

    return particles_list

def update_particles(particles_list):
    pop_particles = []
    for x in range(len(particles_list)):
        particles_list[x][3] = particles_list[x][3] * 0.99
        shift = (particles_list[x][3] - particles_list[x][3] * 0.99) / 2
        particles_list[x][0] += shift + particles_list[x][4]
        particles_list[x][1] += shift + particles_list[x][5]
        particles_list[x][4] = particles_list[x][4] * 0.96
        particles_list[x][5] = particles_list[x][5] * 0.96
        if particles_list[x][3] < 3:
            pop_particles.append(x)

    if len(pop_particles) > 0:
        pop_particles = sorted(pop_particles,reverse=True)
        for x in range(len(pop_particles)):
            particles_list.pop(pop_particles[x])

    return particles_list

def draw_scoreboard(screen,win_scores,player_count,fonts):
    num_to_char_dict = {1:"x",2:"o",3:"r",4:"d"}
    size_pic = x_score_picture.get_width()
    scr_w,scr_h = screen.get_size()
    
    margin_y = 10
    txt_w, txt_h = fonts["score_font"].size("100")
    text_space_x = txt_w * 1.1
    for x in range(player_count):
        screen.blit(eval(num_to_char_dict[x+1]+"_score_picture"),(scr_w-size_pic-text_space_x,scr_h-size_pic*(((-x)+player_count))-margin_y*x))
        set_text(fonts,str(win_scores[x+1]),scr_w-size_pic-text_space_x +size_pic,scr_h-size_pic*(((-x)+player_count))-margin_y*x +round(size_pic/2)-round(txt_h/2),"score_font",screen)
        #pg.draw.circle(screen,(100,100,100),(scr_w-size_pic-text_space_x,scr_h-size_pic*(((-x)+player_count))-margin_y*x),25)

#game variables
turn = 1 #turn 1 = x, turn 2 = o, turn 3 = r, turn 4 = d
win = 0 #when one of player wins
#grid_win_line = [] #line to be drawn when someone wins
grid_change = True #when grid changes (for 1 frame)
grid_size = 3 #grid size 3x3
expand_animation = 0 #animation for expand event (every time) from 0 to 1
expand_animation_start = False #when animation is happening it is True
expand_animation_perf = -1 #perf_counter for animation so it is not frame dependent
grid_expansions = 0 #grid expans grid_expansion times
grid_expanded = 0 #how many times the grid expanded in the current game
deltaTime = 0 #deltaTime

grid = np.zeros((grid_size, grid_size), dtype="int")
spawned_p_win_grid = np.zeros((grid_size, grid_size), dtype="int")
win_grid = np.zeros((grid_size, grid_size), dtype="int")
win_scores = {1:0,2:0,3:0,4:0} #amount of covered areas by players 1-4

line_picture_vert = pg.image.load("line.png").convert_alpha()
line_picture_vert = pg.transform.scale(line_picture_vert,(10,screen_xy))
line_picture_horiz = pg.transform.rotate(line_picture_vert, 90)

line_thin_picture_vert = pg.image.load("line_thin.png").convert_alpha()
line_thin_picture_vert = pg.transform.scale(line_thin_picture_vert,(10,screen_xy))
line_thin_picture_horiz = pg.transform.rotate(line_thin_picture_vert, 90)

x_picture = pg.image.load("x.png").convert_alpha()
o_picture = pg.image.load("o.png").convert_alpha()
r_picture = pg.image.load("r.png").convert_alpha()
d_picture = pg.image.load("d.png").convert_alpha()
x_picture = pg.transform.smoothscale(x_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
o_picture = pg.transform.smoothscale(o_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
r_picture = pg.transform.smoothscale(r_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
d_picture = pg.transform.smoothscale(d_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))

turn_picture_scale = 5
x_turn_picture = pg.image.load("x.png").convert_alpha()
o_turn_picture = pg.image.load("o.png").convert_alpha()
r_turn_picture = pg.image.load("r.png").convert_alpha()
d_turn_picture = pg.image.load("d.png").convert_alpha()

x_turn_picture = pg.transform.smoothscale(x_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))
o_turn_picture = pg.transform.smoothscale(o_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))
r_turn_picture = pg.transform.smoothscale(r_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))
d_turn_picture = pg.transform.smoothscale(d_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))

score_picture_scale = 7
x_score_picture = pg.image.load("x.png").convert_alpha()
o_score_picture = pg.image.load("o.png").convert_alpha()
r_score_picture = pg.image.load("r.png").convert_alpha()
d_score_picture = pg.image.load("d.png").convert_alpha()

x_score_picture = pg.transform.smoothscale(x_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))
o_score_picture = pg.transform.smoothscale(o_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))
r_score_picture = pg.transform.smoothscale(r_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))
d_score_picture = pg.transform.smoothscale(d_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))

stats_picture_scale = 8
x_stats_picture = pg.image.load("x.png").convert_alpha()
o_stats_picture = pg.image.load("o.png").convert_alpha()
r_stats_picture = pg.image.load("r.png").convert_alpha()
d_stats_picture = pg.image.load("d.png").convert_alpha()

x_stats_picture = pg.transform.smoothscale(x_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))
o_stats_picture = pg.transform.smoothscale(o_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))
r_stats_picture = pg.transform.smoothscale(r_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))
d_stats_picture = pg.transform.smoothscale(d_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))

end_game_rect = pg.Surface((600,600),pg.SRCALPHA)
end_game_rect.fill((40,40,40))

logo = pg.transform.scale(pg.image.load("logo.png").convert_alpha(),(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))

arrow_pic_scale = 12
arrow_picture = pg.image.load("arrow.png").convert_alpha()
arrow_picture = pg.transform.scale(arrow_picture,(int(screen_xy/arrow_pic_scale),int(screen_xy/arrow_pic_scale)))
arrow_pic_l = pg.transform.rotate(arrow_picture,-90)
arrow_pic_r = pg.transform.rotate(arrow_picture,90)

arrow_h_picture = pg.image.load("arrow_hover.png").convert_alpha()
arrow_h_picture = pg.transform.scale(arrow_h_picture,(int(screen_xy/arrow_pic_scale),int(screen_xy/arrow_pic_scale)))
arrow_h_pic_l = pg.transform.rotate(arrow_h_picture,-90)
arrow_h_pic_r = pg.transform.rotate(arrow_h_picture,90)

win_picture = pg.image.load("x.png").convert_alpha()

draw_picture = pg.Surface((win_picture.get_size()))
turn_animation = 0 #when animation starts it is set to 1, then goes back to 0
turn_ani_perf = -1
#0 = nothing
#1 = x
#2 = o
#3 = r
#4 = d

reset_game = True

switch_menu = True
menu_type = "main"
menu_type_change = "main"
in_game = False #in_game == False: in menu

btn_list = []
btn_list = append_buttons(btn_list,menu_type)
slider_list = []
slider_percentages = [0,0,0]
slider_list = append_sliders(slider_list,menu_type,slider_percentages)


#button_unhover_pic = pg.image.load("button_unhover.png").convert_alpha()
#button_unhover_pic = pg.transform.scale(button_unhover_pic, (button_width, button_height))
#button_hover_pic = pg.image.load("button_hover.png").convert_alpha()
#button_hover_pic = pg.transform.scale(button_hover_pic, (button_width, button_height))
#title_font = round(screen_width / 14)
#btn_font = title_font - 10

#fonts = {"main_font":pg.font.Font('Roboto-Regular.ttf', title_font),"btn_font":pg.font.Font('Roboto-Regular.ttf', btn_font)}

player_count = 2
tiles_covered = 3 #tiles needed to be covered by 1 player in order to win

blit_x = 0
blit_y = 0

reframe = True #first frame of game: load all images etc.
mouse_down = False
slider_change = False
#menu variables

title_h = 10
clock = pg.time.Clock()
end_game = False #turns to True when end of game
end_game_animation = -1
pause_win_animation_perf = -1 #when end_game_animation is 0.5 this will stop the animation for a brief time

stats_view = 0 #0 is game statistics, 1 for player 1, 2 for 2 etc.

arr_rect_r = pg.Rect((-100,-100),(0,0))
arr_rect_l = pg.Rect((-100,-100),(0,0))

arr_r_hover = False
arr_l_hover = False

reset_confirmed = False #reset in stats menu
reset_perf = -1

copied = False
copied_perf = -1

particles_list = [] #particle: [particle x, particle y, colour, size, vx(4), vy(5)]
particles_perf = -1
p_win_grid = np.zeros((grid_size,grid_size))
playing_complete_sound = False

chnl_music.play(decline_music,loops=-1)

while playing:
    #events
    for e in pg.event.get():
        if e.type == pg.QUIT:
            playing = False

        if e.type == pg.MOUSEMOTION:
            mx, my = pg.mouse.get_pos()
            for i,btn in enumerate(btn_list):
                btn_rect = btn[:4]
                btn_rect = pg.Rect(btn_rect)
                btn_list[i][5] = btn_rect.collidepoint(mx,my)

            for i, slider in enumerate(slider_list):
                slider_rect = slider[:4]
                slider_rect[0], slider_rect[1] = rel_coords(slider[0],slider[1],screenblit)
                slider_rect = pg.Rect(slider_rect)
                if slider_rect.collidepoint(mx,my) and mouse_down:
                    slider_list[i][4] = (mx - slider_rect[0]) / slider_rect[2] * 100
                    slider_change = True
                    slider_percentages[i] = (mx - slider_rect[0]) / slider_rect[2] * 100
            
            if menu_type == 'stats':
                if arr_rect_r.collidepoint(mx,my):
                    arr_r_hover = True
                    arr_l_hover = False

                elif arr_rect_l.collidepoint(mx,my):
                    arr_l_hover = True
                    arr_r_hover = False
                
                else:
                    arr_r_hover = False
                    arr_l_hover = False
                    
        if e.type == pg.VIDEORESIZE:
            screenblit.fill((40,40,40))
            pg.display.flip()
            reframe = True
            
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                if in_game:
                    in_game = False
                    reset_game = True
                else:
                    playing = False
            
            if e.key == pg.K_c:
                if menu_type == "about":#https://discord.gg/wpK3EeSQha
                    pg.scrap.put(pg.SCRAP_TEXT, b"https://discord.gg/wpK3EeSQha")
                    copied = True
                    copied_perf = t.perf_counter()
            
            if e.key == pg.K_s:
                if menu_type == "play":
                    sound = not sound
                    if sound:
                        chnl_sfx.set_volume(0.1)
                        chnl_music.set_volume(0.1)
                    else:
                        chnl_sfx.set_volume(0.0)
                        chnl_music.set_volume(0.0)


            #if e.key == pg.K_UP:
            #    grid = [[2,2,2,2,2],[2,2,2,2,2],[2,2,0,3,3],[3,3,3,3,3],[3,3,3,3,3]]
            #    grid = np.array(grid)
            #    win_grid = np.zeros((5,5))

            #if e.key == pg.K_SPACE:
            #    for x in range(grid.shape[0]):
            #        for y in range(grid.shape[1]):
            #            grid[y,x] = 1
            #    grid_change = True

            #if e.key == pg.K_w:
            #    print(x_picture.get_width())
            #    
            #    #particles_list = append_particle(particles_list,100,100,1,10,10,10)

            if e.key == pg.K_LEFT:
                stats_view -= 1
                if stats_view < 0:
                    stats_view = 0
            if e.key == pg.K_RIGHT:
                stats_view += 1
                if stats_view > 4:
                    stats_view = 4
                

        if e.type == pg.MOUSEBUTTONDOWN:
            mouse_down = True
            mx, my = pg.mouse.get_pos()
            mousebtn = pg.mouse.get_pressed()

            if in_game:
                if mousebtn[0]: #left mouse btn
                    mrx, mry = calculate_mouse_pos(mx, my, grid_size, screen_xy, blit_x, blit_y)
                    if mrx > -1 and mry > -1 and mrx < grid_size and mry < grid_size:
                        if grid[mry, mrx] == 0 and win == 0:
                            grid[mry,mrx] = turn
                            stats_dict['blocks_placed'][turn-1] += 1
                            turn_animation = 1
                            turn = turn % player_count + 1
                            grid_change = True

                            chnl_sfx.play(tick_sound)
            
            elif arr_rect_r.collidepoint(mx,my):
                stats_view -= 1
                if stats_view < 0:
                    stats_view = 0
                    
                
            elif arr_rect_l.collidepoint(mx,my):
                stats_view += 1
                if stats_view > 4:
                    stats_view = 4
                
                
            else: #in menu
                for i,btn in enumerate(btn_list):
                    btn_rect = btn[:4]
                    btn_rect = pg.Rect(btn_rect)
                    if btn_rect.collidepoint(mx,my):
                        if btn[4] == "Play":
                            menu_type = "play"
                            switch_menu = True

                        elif btn[4] == "Start":
                            in_game = True
                            menu_type = "main"
                            switch_menu = True
                            reset_game = True
                            screen.fill((40,40,40))
                            
                        elif btn[4] == "Exit":
                            playing = False
                        
                        elif btn[4] == "Back":
                            menu_type = "main"
                            switch_menu = True
                        
                        elif btn[4] == "Stats":
                            menu_type = "stats"
                            switch_menu = True
                        
                        elif btn[4] == "Reset":
                            if reset_confirmed:
                                stats_dict = {'games_won': [0, 0, 0, 0], 'games_lost': [0, 0, 0, 0], 'games_tied': [0, 0, 0, 0], 'blocks_placed': [0, 0, 0, 0], 'area_covered': [0, 0, 0, 0], 'total_map_expansions': 0, 'games_played': 0}
                                reset_confirmed = False
                            else:
                                reset_confirmed = True
                                reset_perf = t.perf_counter()
                            
                        elif btn[4] == "About":
                            menu_type = "about"
                            switch_menu = True

                for i, slider in enumerate(slider_list):
                    slider_rect = slider[:4]
                    slider_rect = pg.Rect(slider_rect)
                    if slider_rect.collidepoint(mx,my):
                        slider_list[i][4] = (mx - slider_rect[0]) / slider_rect[2] * 100
                        slider_change = True
                        
                if switch_menu:
                    btn_list = append_buttons(btn_list, menu_type)
                    slider_list = append_sliders(slider_list,menu_type,slider_percentages)
                    switch_menu = False
                    
        if e.type == pg.MOUSEBUTTONUP:
            mouse_down = False

    if reset_game:
        #game variables
        turn = 1 #turn 1 = x, turn 2 = o
        win = 0 #when one of player wins
        grid_change = True #when grid changes (for 1 frame)
        grid_size = 3 #grid size 3x3
        expand_animation = 0 #animation for expand event (every time) from 0 to 1
        expand_animation_start = False #when animation is happening it is True
        expand_animation_perf = -1 #perf_counter for animation so it is not frame dependent

        grid_expanded = 0

        end_game = False

        grid = np.zeros((grid_size, grid_size), dtype="int")
        win_grid = np.zeros((grid_size, grid_size), dtype="int")
        p_win_grid = np.zeros((grid_size, grid_size), dtype="int")
        spawned_p_win_grid = np.zeros((grid_size, grid_size), dtype="int")
        
        played_complete_sound = False

        end_game_animation = -1
        reset_game = False
        reframe = True
        screenblit.fill((40,40,40))

    if slider_change:
        grid_expansions,player_count,tiles_covered = calc_slider_values(slider_list,grid_expansions,player_count,tiles_covered)
     
    if reframe:
        window_w,window_h = screenblit.get_size()
        screen_width, screen_height = window_w, window_h
        screen_xy = screen_calc(window_w,window_h)
        screen = pg.transform.scale(screen,(screen_xy,screen_xy))
        blit_x = int((window_w-screen_xy) / 2)
        blit_y = int((window_h-screen_xy) / 2)
        screenblit.fill((0,0,0))

        line_picture_vert = pg.image.load("line.png").convert_alpha()
        line_picture_vert = pg.transform.scale(line_picture_vert,(10,screen_xy))
        line_picture_horiz = pg.transform.rotate(line_picture_vert, 90)

        line_thin_picture_vert = pg.image.load("line_thin.png").convert_alpha()
        line_thin_picture_vert = pg.transform.scale(line_thin_picture_vert,(10,screen_xy))
        line_thin_picture_horiz = pg.transform.rotate(line_thin_picture_vert, 90)
        
        x_picture = pg.image.load("x.png").convert_alpha()
        o_picture = pg.image.load("o.png").convert_alpha()
        r_picture = pg.image.load("r.png").convert_alpha()
        d_picture = pg.image.load("d.png").convert_alpha()
        x_picture = pg.transform.smoothscale(x_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
        o_picture = pg.transform.smoothscale(o_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
        r_picture = pg.transform.smoothscale(r_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
        d_picture = pg.transform.smoothscale(d_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))

        title_font = round(screen_width / 14)
        btn_font = round(screen_width / 28)
        stats_font = round(screen_width / 40)
        score_font = round(screen_width / 28)
        about_font = round(screen_width / 65)

        fonts = {"main_font":pg.font.Font('Roboto-Regular.ttf', title_font),"btn_font":pg.font.Font('Roboto-Regular.ttf', btn_font),"stats_font":pg.font.Font('Roboto-Regular.ttf', stats_font),"score_font":pg.font.Font('Roboto-Regular.ttf', score_font),"about_font":pg.font.Font('Roboto-Regular.ttf', about_font)} 
        screenblit.fill((40,40,40))

        x_turn_picture = pg.image.load("x.png").convert_alpha()
        o_turn_picture = pg.image.load("o.png").convert_alpha()
        r_turn_picture = pg.image.load("r.png").convert_alpha()
        d_turn_picture = pg.image.load("d.png").convert_alpha()

        x_turn_picture = pg.transform.smoothscale(x_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))
        o_turn_picture = pg.transform.smoothscale(o_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))
        r_turn_picture = pg.transform.smoothscale(r_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))
        d_turn_picture = pg.transform.smoothscale(d_turn_picture,(int(screen_xy/turn_picture_scale),int(screen_xy/turn_picture_scale)))

        x_score_picture = pg.image.load("x.png").convert_alpha()
        o_score_picture = pg.image.load("o.png").convert_alpha()
        r_score_picture = pg.image.load("r.png").convert_alpha()
        d_score_picture = pg.image.load("d.png").convert_alpha()

        x_score_picture = pg.transform.smoothscale(x_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))
        o_score_picture = pg.transform.smoothscale(o_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))
        r_score_picture = pg.transform.smoothscale(r_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))
        d_score_picture = pg.transform.smoothscale(d_score_picture,(int(screen_xy/score_picture_scale),int(screen_xy/score_picture_scale)))

        x_stats_picture = pg.image.load("x.png").convert_alpha()
        o_stats_picture = pg.image.load("o.png").convert_alpha()
        r_stats_picture = pg.image.load("r.png").convert_alpha()
        d_stats_picture = pg.image.load("d.png").convert_alpha()

        x_stats_picture = pg.transform.smoothscale(x_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))
        o_stats_picture = pg.transform.smoothscale(o_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))
        r_stats_picture = pg.transform.smoothscale(r_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))
        d_stats_picture = pg.transform.smoothscale(d_stats_picture,(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))

        end_game_rect = pg.Surface((screen_xy,screen_xy),pg.SRCALPHA)
        end_game_rect.fill((40,40,40))

        arrow_picture = pg.image.load("arrow.png").convert_alpha()
        arrow_picture = pg.transform.scale(arrow_picture,(int(screen_xy/arrow_pic_scale),int(screen_xy/arrow_pic_scale)))
        arrow_pic_l = pg.transform.rotate(arrow_picture,-90)
        arrow_pic_r = pg.transform.rotate(arrow_picture,90)

        arrow_h_picture = pg.image.load("arrow_hover.png").convert_alpha()
        arrow_h_picture = pg.transform.scale(arrow_h_picture,(int(screen_xy/arrow_pic_scale),int(screen_xy/arrow_pic_scale)))
        arrow_h_pic_l = pg.transform.rotate(arrow_h_picture,-90)
        arrow_h_pic_r = pg.transform.rotate(arrow_h_picture,90)

        logo = pg.transform.scale(pg.image.load("logo.png").convert_alpha(),(int(screen_xy/stats_picture_scale),int(screen_xy/stats_picture_scale)))

        pause_win_animation_perf = -1

        reframe = False
    
    #calculate stuff
    if in_game:
        if grid_change:
            if not 0 in grid and grid_size < 17 and grid_expanded < grid_expansions + 1:
                if grid_expanded >= grid_expansions:
                    end_game = True
                else:
                    grid_expanded += 1
                    expand_animation_start = True
                
            win, grid_win_line, win_grid, win_scores, p_win_grid = calculate_if_row(grid,grid_size, win_grid,tiles_covered,p_win_grid)

            if tiles_covered > 2:
                for i in range(1,player_count+1):
                    if win_scores[i] >= tiles_covered:
                        end_game = True
                        break

            if end_game and end_game_animation == -1:
                win, grid_win_line, win_grid, win_scores, p_win_grid = calculate_if_row(grid,grid_size, win_grid,tiles_covered,p_win_grid,True)
                end_game_animation = 1
                char_to_num_dict = {'x':1,'o':2,'r':3,'d':4}
                if win != 0:
                    if len(str(win)) > 1: #draw
                        margin_draw = 15
                        width = len(str(win)) * 200 + (len(str(win))-2) * margin_draw + 1
                        draw_picture = pg.Surface((width, 200), pg.SRCALPHA)
                        for x in range(len(str(win))):
                            pic_blit = pg.image.load(str(list(str(win))[x])+".png").convert_alpha()
                            pic_blit = pg.transform.smoothscale(pic_blit,(200,200))
                            draw_picture.blit(pic_blit,(x*200+(x-1)*margin_draw,0))
                            stats_dict['games_tied'][char_to_num_dict[str(list(str(win))[x])]-1] += 1
                        
                        #chnl_sfx.play(draw_sound)

                    else:#one player win
                        win_picture = pg.image.load(win+".png").convert_alpha()
                        win_picture = pg.transform.smoothscale(win_picture,(200,200))
                        stats_dict['games_won'][char_to_num_dict[win]-1] += 1

                        for x in range(1,player_count+1):   
                            if x != char_to_num_dict[win]:
                                stats_dict['games_lost'][x-1] += 1
                        
                        #chnl_sfx.play(complete_sound)
                else:
                    pass
                    #chnl_sfx.play(draw_sound)

                stats_dict['games_played'] += 1
                
                #playing_complete_sound = True
            
        if end_game_animation <= 0.7 and played_complete_sound == False and end_game == True:
            if win != 0:
                if len(str(win)) > 1: #draw
                    chnl_sfx.play(draw_sound)
                else:
                    chnl_sfx.play(complete_sound)
            else:
                chnl_sfx.play(draw_sound)

            playing_complete_sound = True
            played_complete_sound = True

        if end_game_animation <= 0 and end_game == True:
            grid_expansions = 0
            grid_expanded = 0
            in_game = False
            menu_type = "main"
            menu_type_change = True
            end_game = False

        if expand_animation_start:
            if t.perf_counter() > expand_animation_perf + 0.01:
                expand_animation += 0.01
                if expand_animation > 0.25 and expand_animation < 0.26: #only runs once
                    stats_dict['total_map_expansions'] += 1
                    grid, spawned_p_win_grid, grid_size = convert_grid(grid,spawned_p_win_grid,grid_size)
                    x_picture = pg.image.load("x.png").convert_alpha()
                    o_picture = pg.image.load("o.png").convert_alpha()
                    r_picture = pg.image.load("r.png").convert_alpha()
                    d_picture = pg.image.load("d.png").convert_alpha()
                    x_picture = pg.transform.scale(x_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
                    o_picture = pg.transform.scale(o_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
                    r_picture = pg.transform.scale(r_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))
                    d_picture = pg.transform.scale(d_picture, (int(screen_xy/grid_size),int(screen_xy/grid_size)))

                    win_grid = np.zeros((grid_size, grid_size))
                    p_win_grid = np.zeros((grid_size, grid_size))
                    p_spawned_win_grid = np.zeros((grid_size,grid_size))

                    win_scores = {1:0,2:0,3:0,4:0} #amount of covered areas by players 1-4
                    win, grid_win_line, win_grid, win_scores, p_win_grid = calculate_if_row(grid,grid_size, win_grid,tiles_covered,p_win_grid)
                
                if expand_animation > 1: #end of animation
                    expand_animation_start = False
                    expand_animation = 0
                    x_picture.set_alpha(255)
                    o_picture.set_alpha(255)
                    line_picture_vert.set_alpha(255)
                    line_picture_horiz.set_alpha(255)

        #update game screen
        screen.fill((40,40,40))
        screenblit.fill((40,40,40))
        draw_grid(screen, grid, grid_size, win_grid, expand_animation, screen_xy)

    else: #in menu
        if menu_type == 'stats':
            if t.perf_counter() > reset_perf + 3:
                reset_confirmed = False
        elif menu_type == 'about':
            if t.perf_counter() > copied_perf + 3:
                copied = False 
        screenblit.fill((40,40,40))

    #end of frame stuff
    grid_change = False
    
    #spawn particles
    grid_square = round(screen_xy/grid_size)
    playsound = False
    for x in range(win_grid.shape[1]):
        for y in range(win_grid.shape[0]):
            if spawned_p_win_grid[y][x] == 0 and p_win_grid[y][x] > 0:#(particles_list, x, y, p_type, start_size,vx,vy)
                particles_list = append_particle(particles_list,x*grid_square+blit_x,y*grid_square+blit_y,win_grid[y][x],screen_xy/grid_size)
                p_win_grid[y][x] = 0
                spawned_p_win_grid[y][x] = 1 #makes sure that no more spawning happens for the same tile
                playsound = True
    
    if playsound and not playing_complete_sound:
        chnl_sfx.play(win_sound)
    elif playing_complete_sound:
        playing_complete_sound = False

    if in_game:
        screenblit.blit(screen, (blit_x,blit_y))
        draw_scoreboard(screenblit,win_scores,player_count,fonts)
        turn_animation,turn_ani_perf = draw_turn(screenblit, turn,turn_animation,turn_ani_perf,player_count)
        if end_game_animation > 0 and end_game == True: #in end game animation
            end_game_animation,pause_win_animation_perf = draw_end_game(screenblit,fonts,win,end_game_animation,pause_win_animation_perf)

    else:
        btn_list, slider_list, title_h, arr_rect_r, arr_rect_l = draw_menu(screenblit, menu_type, fonts, btn_list, slider_list,grid_expansions,player_count,tiles_covered,title_h,stats_view,stats_dict,reset_confirmed,copied,sound)

    draw_particles(screenblit,particles_list)
    if t.perf_counter() > particles_perf + 0.05:
        particles_list = update_particles(particles_list)


    deltaTime = clock.tick(60) #max of 60 fps
    pg.event.pump()
    pg.display.flip()
    
f = open("scores.txt","w")
f.write(str(stats_dict))
f.close()

#pg.scrap.quit()
pg.font.quit()
pg.quit()
