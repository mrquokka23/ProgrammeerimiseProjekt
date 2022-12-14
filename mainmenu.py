import pygame

pygame.init()

screen_width = 486
screen_height = 564
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menüü")

font = pygame.font.Font("./assets/font.otf", 100) 
colour = {"White": (255,255,255), "Red": (255,0,0), "Rectangle": (59,52,152)}
bgimg = pygame.transform.scale(pygame.image.load("./assets/heiki.jpg"), (486, 564))

def tekst(text, font, text_colour, x, y):

    font_img = font.render(text, True, text_colour)
    screen.blit(font_img, (x,y))
    
run = True

while run:
    mouse = pygame.mouse.get_pos()
    screen.blit(bgimg, (0,0))
    #screen.fill((70,50,90))
    pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(180, 50, 135, 105))
    pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(135, 170, 225, 110))
    pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(135, 300, 230, 110))
    pygame.draw.rect(screen, colour["Rectangle"], pygame.Rect(180, 430, 135, 105))
    tekst("Play", font, colour["White"], 190, 40)
    tekst("Options", font, colour["White"], 145, 160)
    tekst("Replays", font, colour["White"], 145, 290)
    tekst("Quit", font, colour["White"], 190, 420)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen_width/2-60 <= mouse[0] <= screen_width/2+60 and screen_height/2 - 225 <= mouse[1] <= screen_height/2 - 145: #play
                tekst("Play", font, colour["Red"], 585, 100)
                print("Play")

            if screen_width/2-100 <= mouse[0] <= screen_width/2+120 and screen_height/2 - 105 <= mouse[1] <= screen_height/2 - 20: #options
                tekst("Options", font, colour["Red"], 540, 250)
                print("Options")

            if screen_width/2-95 <= mouse[0] <= screen_width/2+115 and screen_height/2 + 20 <= mouse[1] <= screen_height/2 + 100: #replay
                tekst("Replays", font, colour["Red"], 540, 400)
                print("Replays")

            if screen_width/2-60 <= mouse[0] <= screen_width/2+60 and screen_height/2 + 150 <= mouse[1] <= screen_height/2 + 230: #exit
                tekst("Quit", font, colour["Red"], 585, 550)
                run = False
                
            
    pygame.display.update()
pygame.quit()