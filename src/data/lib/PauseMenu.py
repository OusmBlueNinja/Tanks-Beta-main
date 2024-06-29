import pygame, sys

from data.lib import button

from pygame.locals import *

def blur_surface(surface):
      
      # Adjust blur amount (higher value = more blur)
      blur_amount = 2

      # Create a copy to avoid modifying the original surface
      blurred_surface = surface.copy()
      # Apply blur filter (experiment with different filter types)
      blurred_surface = pygame.transform.smoothscale(blurred_surface, 
                                                     (int(surface.get_width() / blur_amount), 
                                                      int(surface.get_height() / blur_amount)))
      blurred_surface = pygame.transform.smoothscale(blurred_surface, surface.get_size())
      return blurred_surface


def debug(data, sevarity: int):

    class b:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\u001b[31m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        WHITE = '\u001b[37m'
    if sevarity == 0:
        print(f'\r{b.OKGREEN}[OUTPUT]{b.ENDC} {data}')

    elif sevarity == 2:
        print(f'\r{b.WARNING}[WARNING]{b.ENDC} {data}')
    elif sevarity == 3:
        print(f"\r{b.FAIL}[ERROR]{b.ENDC} {data}")
    elif sevarity == 4:
        print(f'\r{b.OKBLUE}[INFO]{b.ENDC} {data}                    ', end="")
    


def PauseGameLoop(display, PauseImg, paused):
    # Fill the display with a semi-transparent black background for a dimming effect
      display.fill((0, 0, 0, 128))  # Adjust alpha value for desired transparency

      # Pause music (unchanged)
      if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

      # Show mouse cursor (unchanged)
      if not pygame.mouse.get_visible():
        pygame.mouse.set_visible(True)

      # Event loop (unchanged)
      for event in pygame.event.get():
        # Handle quit event (unchanged)
            if event.type == QUIT:
                #save.save((player_rect.x), (player_rect.y))
                print('\n')
                debug("Closing Program with exit code 0", 2)
                pygame.quit()
                sys.exit()
                
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    debug("UnPaused", 4)
                    return not paused

      # Blur the display surface (new)
      blurred_display = blur_surface(display)

      # Draw paused overlay on top of the blurred background (unchanged)
      
      display.blit(blurred_display, (0, 0))
      display.blit(PauseImg, (0, 0))
      return paused
      
      
      