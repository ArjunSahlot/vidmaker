import pygame
import vidmaker

FPS = 60

WINDOW = pygame.display.set_mode((300, 300))
# If fps and resolution are auto then late_export has to be True
video = vidmaker.Video("vidmaker.mp4", late_export=True)
pygame.display.set_caption("vidmaker test")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        window.fill((255, 0, 0))
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and ctrl_pressed:
                    pygame.quit()
                    return

        # set inverted=True if your colors are inverted
        video.update(pygame.surfarray.pixels3d(window).swapaxes(0, 1), inverted=False)
        pygame.display.update()


main(WINDOW)
video.export(True)
