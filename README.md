# vidmaker

A python library which simplifies creating and exporting videos.

## Purpose

vidmaker was created because I wanted to record some of my pygame projects, and I found this to be the most convenient way.

## How to use

NOTE: vidmaker uses temporary disk space to store frames. This prevents over usage of memory, but slows it down

Since this is a python library, install it by `pip install vidmaker`

Currently vidmaker only has one class, `Video`, making it extremely simple to use.

First, you have to initialize your video with the path you want it to render at the fps and the resolution\*. Always include the ".mp4" ending to the path, vidmaker DOES NOT do it for you.

```py
import vidmaker

video = vidmaker.Video(path="vidmaker.mp4", fps=60, resolution="AUTO")
```

Then you have to update the video every frame with the image you want it to add to your video.

```py
import pygame
import vidmaker

FPS = 60

WINDOW = pygame.display.set_mode((300, 300))
video = vidmaker.Video("vidmaker.mp4", FPS)
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

        video.update(pygame.surfarray.pixels3d(window).swapaxes(0, 1))  # THIS LINE
        pygame.display.update()


main(WINDOW)
```

Once your program finishes, you just have to export your video

```py
video.export(verbose=True)
```

That's it! You should find your video fully rendered at the given path, but the longer the video, the longer `video.export()` takes. I tested this example at over 1000fps during exporting on my computer and it should be even faster without verbose. The speed does heavily depend of what you are exporting and your computer.

## Contributing

Contributing is always appreciated! I would love it if anyone was to make a pull request to add another feature or create an issue post. Possible features could be things like an option to use memory instead of disk space, the option to render videos in different formats (only mp4 right now), and many more. If there is enough demand I might add some myself as well. Thanks for the support!
