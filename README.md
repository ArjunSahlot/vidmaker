# vidmaker

A python library which simplifies creating and exporting videos.

## Purpose

vidmaker was created because I wanted to record some of my pygame projects, and I found this to be the most convenient way.

## How to use

NOTE: vidmaker uses temporary disk space to store frames. This prevents over usage of memory, but slows it down

Since this is a python library, install it by `pip install vidmaker`

Currently vidmaker only has one class, `Video`, making it extremely simple to use.

First, you have to initialize your video with the path you want it to render at the fps and the resolution\*

```py
import vidmaker

video = vidmaker.Video(path=".", fps=60, resolution="AUTO")
```

Then you have to update the video every frame with the image you want it to add to your video.

```py
import pygame
import vidmaker

FPS = 60

# Window Management
WINDOW = pygame.display.set_mode((300, 300))
video = vidmaker.Video(".", FPS)
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

        video.update(pygame.surfarray.pixels3d(window))  # THIS LINE
        pygame.display.update()


main(WINDOW)
```

Once your program finishes, you just have to export your video

```py
video.export()
```

That's it! You should find your video fully rendered at the given path, but the longer the video, the longer `video.export()` takes.
