import pygame as pg
pg.init()
screen = pg.display.set_mode((600,600),pg.RESIZABLE)
playing = True
pg.display.set_caption("template")

while playing:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            playing = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                playing = False
            if e.key == pg.K_w:
                print("w")
                pg.scrap.init()
                pg.scrap.put(pg.SCRAP_TEXT, b"A text to copy")
                #pg.scrap.put("Plain text", b"Data for user defined type 'Plain text'")
        pg.event.pump()

        mx, my = pg.mouse.get_pos()
        screen.fill((0,0,0))
        pg.draw.circle(screen,(255,255,255),(mx,my),5)
        pg.display.flip()

pg.quit()
