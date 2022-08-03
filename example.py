import pygame
import vidmaker

FPS = 60

# Window Management
WINDOW = pygame.display.set_mode((300, 300))
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

        video.update(pygame.surfarray.pixels3d(window).swapaxes(0, 1))
        pygame.display.update()


main(WINDOW)
video.export(True)
