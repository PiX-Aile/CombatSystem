import pygame
import os # file management

path_images=os.path.join(os.getcwd(),"Images")

win = pygame.display.set_mode((1250,680))
pygame.display.set_caption("Combat")
pygame.init()
#main_font=pygame.font.Font(None,25)

# load images
images_list = {}
for name in os.listdir(path_images):
    if ".png" in name :
        images_list[name.split(".")[0]] = pygame.image.load(os.path.join(path_images, name))
images_list["background"] = pygame.transform.rotozoom(images_list["background"], 0, 0.65)


# drawing function
def draw():
    win.fill((0,0,0))
    win.blit(images_list["background"], (0,0))
    pygame.display.update()


# main loop
while 1:
    draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        quit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
