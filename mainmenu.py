import pygame
import os

local_dir = os.path.dirname(__file__)



def tekst(text, text_colour, x, y, screen, fontsize=100):
    font = pygame.font.Font(local_dir + "/assets/font.otf", fontsize) 
    font_img = font.render(text, True, text_colour)
    screen.blit(font_img, (x,y))

def options(screen, colour):
    run = True
    no_of_generations = 500
    while run:
        screen.fill((39, 39, 42))
        tekst("Options", colour["White"], 100, 100, screen, fontsize=50)
        tekst("Back", colour["White"], 100, 500, screen, fontsize=50)
        tekst("Number of generations:", colour["White"], 100, 200, screen, fontsize=50)
        tekst("<", colour["White"], 100, 250, screen, fontsize=50)
        tekst(">", colour["White"], 300, 250, screen, fontsize=50)
        tekst(str(no_of_generations), colour["White"], 200, 250, screen, fontsize=50)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 100 <= mouse[0] <= 130 and 250 <= mouse[1] <= 300 and no_of_generations >= 20:
                    no_of_generations -= 10
                if 300 <= mouse[0] <= 330 and 250 <= mouse[1] <= 300 and no_of_generations <= 1000:
                    no_of_generations += 10
                if 100 <= mouse[0] <= 130 and 500 <= mouse[1] <= 550:
                    return no_of_generations
        pygame.display.update()
    return no_of_generations

def replays(screen, colour):
    run = True
    i = 0
    while run:
        files = []
        for file in os.listdir(local_dir + "/replays"):
            if file.endswith(".pkl"):
                files.append(file)

        screen.fill((39, 39, 42))
        tekst("Replays", colour["White"], 100, 100, screen, fontsize=50)
        tekst("Trained ai-s", colour["White"], 100, 200, screen, fontsize=50)
        tekst("<", colour["White"], 100, 300, screen, fontsize=50)
        tekst(">", colour["White"], 400, 300, screen, fontsize=50)
        tekst(files[i], colour["White"], 150, 300, screen, fontsize=50)
        tekst("Replay ->", colour["White"], 100, 400, screen, fontsize=50)
        tekst("Back", colour["White"], 100, 500, screen, fontsize=50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 100 <= mouse[0] <= 130 and 500 <= mouse[1] <= 550:
                    return None
                if 100 <= mouse[0] <= 130 and 300 <= mouse[1] <= 350 and i > 0:
                    i -= 1
                if 400 <= mouse[0] <= 430 and 300 <= mouse[1] <= 350 and i < len(files)-1:
                    i += 1
                if 100 <= mouse[0] <= 200 and 400 <= mouse[1] <= 450:
                    return files[i]
                
        pygame.display.update()

def mainmenu():
    pygame.init()

    screen_width = 486
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menüü")


    colour = {"White": (255,255,255), "Red": (255,0,0), "Rectangle": (239, 68, 68)}
    bgimg = pygame.transform.scale(pygame.image.load(local_dir + "/assets/heiki.jpg"), (100, 100))
    options_list = [500]
    run = True
    while run:
        mouse = pygame.mouse.get_pos()
        screen.fill((39, 39, 42))
        screen.blit(bgimg, (screen_width-150, screen_height-150))
        pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(180, 50, 135, 105), border_radius=10)
        pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(135, 170, 225, 110), border_radius=10)
        pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(135, 300, 230, 110), border_radius=10)
        pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(135, 430, 230, 110), border_radius=10)
        pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(180, 560, 135, 105), border_radius=10)
        tekst("Sponsored by - Heiki", colour["White"], screen_width-100-250, screen_height-115, screen, fontsize=30)
        tekst("Play", colour["White"], 190, 40, screen)
        tekst("Train AI", colour["White"], 145, 160, screen)
        tekst("Options", colour["White"], 145, 290, screen)
        tekst("Replays", colour["White"], 145, 420, screen)
        tekst("Quit", colour["White"], 190, 550, screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 180 <= mouse[0] <= 180+135 and 50 <= mouse[1] <= 50+105: #play
                    tekst("Play", colour["Red"], 585, 100, screen)
                    pygame.quit()
                    return(("Play"))
                
                if 135 <= mouse[0] <= 135+225 and 170 <= mouse[1] <= 170+110: #play ai
                    tekst("Train ai", colour["Red"], 540, 250, screen)
                    return(("Train ai", options_list[0]))


                if 135 <= mouse[0] <= 135+230 and 300 <= mouse[1] <= 300+110: #options
                    tekst("Options", colour["Red"], 540, 400, screen)
                    options_list[0] = options(screen, colour)
                    

                if 135 <= mouse[0] <= 135+230 and 430 <= mouse[1] <= 430+110: #replay
                    tekst("Replays", colour["Red"], 540, 550, screen)
                    tmp = replays(screen, colour)
                    if tmp != None:
                        return(("Replay", tmp))

                if 180 <= mouse[0] <= 180+135 and 550 <= mouse[1] <= 550+105: #exit
                    tekst("Quit", colour["Red"], 585, 700, screen)
                    run = False
                    
                
        pygame.display.update()
