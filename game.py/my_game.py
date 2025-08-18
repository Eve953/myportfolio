import pygame


pygame.init()


window = pygame.display.set_mode((600, 600))

pygame.mixer.init()
pygame.mixer.music.load('whoosh.mp3')
pygame.mixer.music.play(-1)

running = True

def main():
    clock = pygame.time.Clock()
    running = True
    x = 300
    y = 300
    velocity = 10

    while running:
        clock.tick(80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        window.fill((147, 112, 219))
        pygame.draw.circle(window, "red", (x,y), 50)
        
   
        x+=velocity

        if  x>580 or x <20:
            velocity= -velocity


        pygame.display.update()

    pygame.quit()
    

main()