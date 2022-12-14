import pygame

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menüü")

font = pygame.font.Font("ProgrammeerimiseProjekt/assets/font.otf", 100) 
colour = {"White": (255,255,255), "Red": (255,0,0)}
bgimg = pygame.transform.scale(pygame.image.load("ProgrammeerimiseProjekt/assets/heiki.jpg"), (1280, 720))

def tekst(text, font, text_colour, x, y):

    font_img = font.render(text, True, text_colour)
    screen.blit(font_img, (x,y))
    
run = True

while run:
    mouse = pygame.mouse.get_pos()
    screen.blit(bgimg, (0,0))
    #screen.fill((70,50,90))
    tekst("Play", font, colour["White"], 585, 100)
    tekst("Options", font, colour["White"], 540, 250)
    tekst("Replays", font, colour["White"], 540, 400)
    tekst("Quit", font, colour["White"], 585, 550)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen_width/2-60 <= mouse[0] <= screen_width/2+60 and screen_height/2 - 240 <= mouse[1] <= screen_height/2 - 160: #play
                tekst("Play", font, colour["Red"], 585, 100)
                print("Play")

            if screen_width/2-100 <= mouse[0] <= screen_width/2+120 and screen_height/2 - 90 <= mouse[1] <= screen_height/2 - 10: #options
                tekst("Options", font, colour["Red"], 540, 250)
                print("Options")

            if screen_width/2-100 <= mouse[0] <= screen_width/2+120 and screen_height/2 + 60 <= mouse[1] <= screen_height/2 + 140: #replay
                tekst("Replays", font, colour["Red"], 540, 400)
                print("Replays")

            if screen_width/2-60 <= mouse[0] <= screen_width/2+60 and screen_height/2 + 210 <= mouse[1] <= screen_height/2 + 290: #exit
                tekst("Quit", font, colour["Red"], 585, 550)
                run = False
            
            
    pygame.display.update()
pygame.quit()