import os
import time
LoadTime = time.time()
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import json
import random
import sys
import pygame
from pygame.locals import *

# 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


global path
# get the current working directory
path = os.path.dirname(os.path.abspath(__file__))

f = open(f'{path}\\data\\config\\config.json')
data = json.load(f)
DEBUG = data['config']['debug']



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
        print(f'\r{b.OKBLUE}[INFO]{b.ENDC} {data}', end="")
    elif DEBUG:
        if sevarity == 1:
            print(f'\r{b.OKCYAN}[DEBUG]{b.ENDC} {data}')


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


clock = pygame.time.Clock()


debug("Loading Config", 1)
# get Config Files
f2 = open(f'{path}\\data\\config\\config.json')
data = json.load(f2)
f2 = open(f'{path}\\data\\config\\settings.json')
data2 = json.load(f2)
resoloution = data2['Resolution']
playMusic = data2['Music']
DrawTrees = data2['DrawTrees']
width, height = data['config']['resolutions'][resoloution]['width'], data['config']['resolutions'][resoloution]['height']
WindowName = data['config']['name']
Version = data['config']['version']
RenderDistance = data['config']['Render-Distance']
AmountOfTrees = data['config']['trees']


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # initiates pygame
pygame.mixer.set_num_channels(64)
pygame.mouse.set_visible(data2['HideCursor'])

pygame.display.set_caption(WindowName + " " + Version)

WINDOW_SIZE = (width, height)

SURFACE_SIZE = (720, 480)
#SURFACE_SIZE = (1280, 720)

#
# -----------------------------------
#




Velocity = 150


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window


display = pygame.Surface(SURFACE_SIZE)  # used as the surface for rendering, which is scaled
#display = pygame.Surface((1290, 720))

###########################
#       Load Assets       #
###########################
assets = "/assets"
sound = "/sound"
music = "/music"
tools = "/tools"
entities = "/entities"
images = "/images"
world = "/world"






debug(f"Loading Sounds",1)

songs = [
                    "//assets//sound//music//(1).wav",
                    "//assets//sound//music//(2).wav",
                    "//assets//sound//music//(3).wav",
                    "//assets//sound//music//(4).wav",
                    "//assets//sound//music//(5).wav"
                ]

try:
  if playMusic:
    
  
    pygame.mixer.music.load(f'{path}{songs[random.randint(0,(len(songs)-1))]}')
    pygame.mixer.music.set_volume(0.2)
    
    pygame.mixer.music.play()  
    debug(f"Songs Loaded", 1)
            
except:
  debug(f'Unable to find song files, {path}//src//assets//sound//', 3)  
  debug(f'Process ednded with code 1', 3)
  pygame.quit()
  sys.exit()
#debug("Loading scope_img",1)
# scope_img = pygame.image.load(
#    f'{path}//{assets}//{images}//{entities}//scope.png')
#debug("Loading treeSmall",1)
# treeSmall = pygame.image.load(
#    f'{path}//{assets}//{images}//{world}//treeSmall.png')


class SpriteSheet():
	def get_image(self, frame, width, height, scale, colour, sheet):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image


sprite_sheet = SpriteSheet()


allAssets = []
AnimationAssets = []
ActiveAnimations = []


# file name | folder name

# asset loader 
assetList = [
                ["scope", "entities"],
                ["treeSmall", "world"],
                ["tankGreen", "entities"],
                ["barrelGreen", "entities"],
                ["tracksSmall", "entities"],
                ["dirt", "world"],
                ["Barrels", "world"],
                ["barrelGreen_up", "world"],
                ["tracksSmall","entities"]
                
            ]


# Filename | folder name | Frame Size | Frame Length
AnimationAssetList = [
    ["Explosions", "world", 96, 12],
]

logo = pygame.image.load(f'{path}//assets//images//WindowLogo.png')

pygame.display.set_icon(logo)


for i in range(len(assetList)):
    debug(f"Loading \x1b[38;5;26m{assetList[i][0]}", 1)
    try:
        allAssets.append(pygame.image.load(
            f'{path}//{assets}//{images}//{assetList[i][1]}//{assetList[i][0]}.png'))
    except:
        debug(f'Unable to find {assetList[i][0]}', 3)


for i in range(len(AnimationAssetList)):
    try:
        debug(f"Loading Animation \x1b[38;5;39m{AnimationAssetList[i][0]}", 1)
        AnimationAssets.append(pygame.image.load(
            f'{path}//{assets}//{images}//{AnimationAssetList[i][1]}//{AnimationAssetList[i][0]}.png'))
    except:
        debug(f'Unable to find Animation {AnimationAssetList[i][0]}', 3)

AnimationFrameList = []
current = 0
for i in AnimationAssetList:
    currentAnimation = []
    try:
        debug(f"Seperating Animation Frames \x1b[38;5;75m{AnimationAssetList[current][0]}", 1)
        for frameNum in range(i[3]):
            currentAnimation.append(sprite_sheet.get_image(frameNum, i[2], i[2], 1, (0,0,0), AnimationAssets[current]))
        
        AnimationFrameList.append(currentAnimation)
    except Exception as e:
        debug(f'Unable to Seperate Animation Frames {AnimationAssetList[current][0]} | {e}', 3)
    current += 1
del current


###########################
#      Set FX Volume      #
###########################

FX = [
    "Boom",
    ]



def PlaySoundEffect(id:int):
    try:
        pygame.mixer.Sound(f'{path}//{assets}//{sound}//{FX[id]}.wav').play()
    except Exception as e:
        debug(f'Unable to Play Sound Effect {FX[id]} | {e}', 3)


pygame.mixer.music.set_volume(0.5)


###########################
#      Entity Classes    #
###########################
def drawBar(Lable: str, Value:int, Position:tuple, Size:int, Color:tuple, DrawText=True):
    pygame.draw.rect(display, (0,0,0), Rect(Position[0],Position[1]-5,210,Size+15))
    pygame.draw.rect(display, Color, Rect(Position[0]+5,Position[1],(Value*2),Size+5))
    text = f"{Lable}: " + str(Value)
    font = pygame.font.Font("freesansbold.ttf", Size)
    text = font.render(text, 1, (255, 255, 255))
    
    # draw rectangle to show FPS
    if DrawText:
        display.blit(text, (Position[0]+5,Position[1]+(Size/5) ))
        



class Entity:
    def __init__(self, x, y, width, height, image, scope):
        self.hp = 100
        self.Armor = 50
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.image = image
        self.scopeImg = scope
        self.Zero = (((SURFACE_SIZE[0]/2)-(75/2)), (SURFACE_SIZE[1]/2)-(70/2))
        self.Gun_image = pygame.transform.rotate(allAssets[3], 0)
        self.offset = [ self.image.get_width() / 2  , self.image.get_height() / 2 ]
        
    # draw the current fps to window
    


    # draw the current frame per second to window
 

    
      

    def WeaponRotation(self, display):
        
        mousePos = pygame.mouse.get_pos()
        
        
        

        rel_x, rel_y = mousePos[0] - self.x, mousePos[1] - self.y
        angle = -math.atan2(self.Zero[1] + self.offset[1]- mousePos[1], self.Zero[0] + self.offset[0] - mousePos[0]) * ( 180 / math.pi )
        angle = angle + 90
        
        #debug(f"{angle}", 0)

        self.Gun_image = pygame.transform.rotate(allAssets[3], angle)
        
        axis = ( (self.Zero[0] - int(self.Gun_image.get_width() / 2 ) + self.offset[0]) , (self.Zero[1] - int(self.Gun_image.get_height() / 2 ) + self.offset[1])  )
        
        pygame.Surface.blit(display, self.Gun_image, axis)
        pygame.Surface.blit(display, self.scopeImg, ((mousePos[0] - 16)*2-(WINDOW_SIZE[0]/2), (mousePos[1] -16 )*2 - (WINDOW_SIZE[1]/2)))

    def main(self, display):
        
        
        pygame.Surface.blit(display, self.image, self.Zero)
        #pygame.Surface.blit(display, self.Trackimage, self.Zero)
        
        
        
    def drawHP(self):
        
        drawBar("Armor",self.Armor, (25, height-75), 10, (50,100,255), False)
        drawBar("HP",self.hp, (25, height-55), 20, (20,255,20))
        
    def Damage(self, ammount:int):
            if self.Armor >= ammount:
                self.Armor -= ammount
            else:
                ammount -= self.Armor
                self.Armor = 0
                self.hp -= ammount
            
            
        
        
        
        
        
    def rotateImage(self, direction: int):
        
        angle = 45 * direction
        
        self.image = pygame.transform.rotate(allAssets[2], angle)
        


# init
# X Y ( Size )
player = Entity(100, 100, 64, 64, allAssets[2], allAssets[0])


###########################
#      Display Scroll     #
###########################
# set to center of feild


scroll = [1000,1000]    




###########################
#       Game Loop         #debug
###########################


rockLock = []
barrelList = []
sbarrelList = []

debug("Generating Map", 1)


casheList=[]

for i in range(4000):
    casheList.append([])

AmoutOfTrees = 0
for x in range(int(4000 / allAssets[1].get_width())):
            for y in range(int(4000 / allAssets[1].get_height())):
                x2 = x
                y2 = y
                x2 = x2 * allAssets[1].get_width()

                y2 = y2 * allAssets[1].get_height()
                
                
                if random.randint(0,100) <= 10:
                    rockLock.append([((x2)), ((y2))])
                    AmoutOfTrees += 1

                                        
                                        

    
for i in range(random.randint(1,3)):
    newBarrel = [random.randint(-0, 2000), random.randint(-0, 2000)]
    barrelList.append(newBarrel)
for i in range(random.randint(1,10)):
    newBarrel = [random.randint(-0, 2000), random.randint(-0, 2000)]
    sbarrelList.append(newBarrel)

class NotGlobal():
    def __init__(self, d, i) -> None:
        self.delay = d
        self.invert = i
        self.dt = 0
        
NotGlobal = NotGlobal(500, False)


#display.blit(textSurface, (SURFACE_SIZE[0]/2-textSurface.get_width()/2,SURFACE_SIZE[1]/2))

def EdgeOfMap():
    # print red test to screen that sais
    # END OF GAME BOUNDS
    text = "END OF GAME BOUNDS"
    font = pygame.font.Font("freesansbold.ttf", 20)
    # print text to display surfacewwwwwwwwwwwwwwwwwwwwwwww
    # find 
    textSurface = font.render(text, False, (255, 0, 0))
    
    player.Damage(1)
    
    # blit to display surface
    
    if NotGlobal.delay >= 400:
        NotGlobal.invert = True
    elif NotGlobal.delay <= -400:
        NotGlobal.invert = False
        
    if NotGlobal.invert:
        NotGlobal.delay -= 999 * NotGlobal.dt
        display.blit(textSurface, (SURFACE_SIZE[0]/2-textSurface.get_width()/2,SURFACE_SIZE[1]/2))
    else:
        NotGlobal.delay += 999 * NotGlobal.dt
    




    

    
    
debug("Map Generated", 1)


TimeThen = time.time()

LoadClear = time.time()
runTime = 0


TimeNow = time.time()
Load = TimeNow - LoadTime
debug(f"Loaded in {Load} Seconds", 1)



def visable(x, y, szex, szey):
    if scroll[0] >= x and scroll[0] <= (x + szex):
            if scroll[1] >= y and scroll[1] <= (y + szey):
                return True
            else:
                return False
    else:
        return False
    
    
oldPos = 0
newPos = 0
i2 = -999


def treepos(x,y):
    if not DrawTrees:
        return False
    if FPS <= 30:
        return False
    valid = False
    for i in range(len(rockLock)):
        if rockLock[i][0] == x and rockLock[i][1] == y:
            valid = True
            break
    
    return valid
    
class GUIdebug:
    def __init__(self):
        self.id = 0
    def NewFrame(self):
        self.id = 0
    def drawDebugText(self, text: any, Format=True, Text="None"):
        
            
        if not Format:
            font = pygame.font.Font("freesansbold.ttf", 20)
            size = (3, 3)
            text = str(text)
        else:
            self.id += 1
            id = self.id
            _id = "P"+str(id)
            #print(Text)
            if Text!="None":
               _id = Text
            
            font = pygame.font.Font("freesansbold.ttf", 15)
            size = (5, ((id*17)+5))
            text = f"({_id}): " + str(text)

        text = font.render(text, 1, (255, 255, 255))
        display.blit(text, size)
        
GUIdebug = GUIdebug()
    

def ShowFPS(display):
        # get current fps
        #of the game
        fps = str(int(clock.get_fps()))
        text = "FPS: " + fps
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(text, 1, (255, 255, 255))

        # draw rectangle to show FPS
        display.blit(text, (10, 10))
        

def get_player_world_position(player_screen_x, player_screen_y, scroll):
  """
  Calculates the player's world position based on screen position and scroll.

  Args:
      player_screen_x: Player's X position on the screen (pixels).
      player_screen_y: Player's Y position on the screen (pixels).
      scroll: Current scroll position (tuple containing X and Y scroll offsets).

  Returns:
      A tuple containing the player's world position (X, Y) in units.
  """

  # Get screen width and height (assuming these are available globally)
  screen_width, screen_height = screen.get_size()

  # Calculate player's offset from screen center (assuming centered player)
  player_offset_x = player_screen_x - screen_width // 2
  player_offset_y = player_screen_y - screen_height // 2

  # Convert offset to world position by adding scroll value
  player_world_x = player_offset_x + scroll[0]
  player_world_y = player_offset_y + scroll[1]

  return player_world_x, player_world_y





    


TestVar = 0
while True:  # game loop
    
    TimeNow = time.time()
    dt = TimeNow - TimeThen
    NotGlobal.dt = dt
    runTime = TimeNow - LoadClear
    TimeThen = time.time()
    FPS = clock.get_fps()
    
    display.fill((189,137,88))  # clear screen by filling it with blue

    #mousePos = pygame.mouse.get_pos()
    # debug(mousePos)

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            #save.save((player_rect.x), (player_rect.y))
            print('\n')
            debug("Closing Program with exit code 0", 2)
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    keysDown = ["   ","  ","  ","  "]
    angle = 0
    if keys[pygame.K_a]:
        angle -= 90
        scroll[0] -= Velocity * dt
        keysDown[1] = "a"
        player.rotateImage(2)
    if keys[pygame.K_d]:
        angle += 90
        scroll[0] += Velocity * dt
        keysDown[3] = "d"
        player.rotateImage(6)
    if keys[pygame.K_w]:
        angle -= 0
        scroll[1] -= Velocity * dt
        keysDown[0] =  "w"
        player.rotateImage(0)
    if keys[pygame.K_s]:
        angle -= 180
        scroll[1] += Velocity * dt  
        keysDown[2] =  "s"
        player.rotateImage(4)
    if keys == None:
        player.rotateImage(0)
        
    
        
    
    objects = 0 
    # Draw Bacround
    if 1:
        for x in range(int(4000 / allAssets[5].get_width())):
            for y in range(int(4000 / allAssets[5].get_height())):
                x2 = x
                y2 = y
                x2 = x2 * allAssets[5].get_width()

                y2 = y2 * allAssets[5].get_height()

                if x2-scroll[0] > 0 - allAssets[5].get_width():
                    if y2-scroll[1] > 0 - allAssets[5].get_height():
                        if (x2-scroll[0]) - 200 < RenderDistance[0] - allAssets[5].get_width():
                            if (y2-scroll[1]) - 200 < RenderDistance[1] - allAssets[5].get_height():
                                objects += 1
                                pygame.Surface.blit(display, allAssets[5], (((x2-scroll[0])), ((y2-scroll[1]))))
                                #print(x2, y2)
                    #print((((i-scroll[0])), ((i-scroll[1]))))
    
    #Draw Trees  
    
    if 1:
        for x in range(int(4000 / allAssets[1].get_width())):
            for y in range(int(4000 / allAssets[1].get_height())):
                x2 = x
                y2 = y
                x2 = x2 * allAssets[1].get_width()

                y2 = y2 * allAssets[1].get_height()
                
                if treepos(((x2)), ((y2))):
                    

                    if x2-scroll[0] > 0 - allAssets[1].get_width():
                        if y2-scroll[1] > 0 - allAssets[1].get_height():
                            if (x2-scroll[0]) - 125< RenderDistance[0] - allAssets[1].get_width():
                                if (y2-scroll[1]) - 125 < RenderDistance[1] - allAssets[1].get_height():

                                        objects += 1
                                        pygame.Surface.blit(display, allAssets[1], (((x2-scroll[0])), ((y2-scroll[1]))))

        
    for i in range(len(barrelList)):
        currentBarrel = pygame.transform.rotate(allAssets[6], random.randint(0,364))
        objects += 1
        pygame.Surface.blit(display, allAssets[6], ((barrelList[i][0]-scroll[0]), (barrelList[i][1]-scroll[1])))
    for i in range(len(sbarrelList)):
        objects += 1
        currentBarrel = pygame.transform.rotate(allAssets[7], random.randint(0,364))
        pygame.Surface.blit(display, allAssets[7], ((sbarrelList[i][0]-scroll[0]), (sbarrelList[i][1]-scroll[1])))
        
        
        
    
    
    
    player.main(display)
    player.WeaponRotation(display)
    
    
    

    if not pygame.mixer.music.get_busy() and playMusic:
        
        debug(f"Loading Sounds",1)

        songs = [
                            "//assets//sound//music//(1).wav",
                            "//assets//sound//music//(2).wav",
                            "//assets//sound//music//(3).wav",
                            "//assets//sound//music//(4).wav",
                            "//assets//sound//music//(5).wav"
                        ]
        
        try:
          currentSong= random.randint(0,(len(songs)-1))
          pygame.mixer.music.load(f'{path}{songs[currentSong]}')
          pygame.mixer.music.set_volume(0.2)
          
          # ___________________________
          if playMusic:
            pygame.mixer.music.play()  
          
          ## UNCOMENT ME  /\ /\ /\ 
          debug(f"Songs Loaded", 1)
                    
        except:
          debug(f'Unable to find song files, {path}//src//assets//sound//', 3)  
          debug(f'Process ednded with code 1', 3)
          pygame.quit()
          sys.exit()

    

    
    if FPS < 30 and runTime > 2:
        debug(
            f"High Frame Render Time, it takes {dt} sconds to render a frame.  fps: {FPS}", 2)
    #debug(f'FPS: {FPS}', 4)

    
    #debug(f"{dt}", 1)
    
    
    
    
    
    
    
    
    
    if scroll[1] >= 2000:
        EdgeOfMap()
        scroll[1] = 1999
    if scroll[1] <= -1:
        EdgeOfMap()
        scroll[1] = -0   
    if scroll[0] >= 2000:
        EdgeOfMap()
        scroll[0] = 1999
    if scroll[0] <= -1:
        EdgeOfMap()
        scroll[0] = -0  
        
    
    # Flag to track if an animation is already spawning
    # Flag to track if an animation is already spawning
    spawn_animation = False
    is_world_coordinates = True  # Initial state assuming screen coordinates by default


    if pygame.mouse.get_pressed()[0] == 1 and not spawn_animation:
        CanFire = True
        for animation in ActiveAnimations:
            if animation[5] == "SHOT":
                CanFire = False
        if CanFire:
            # Get mouse position (assuming screen coordinates)
            world_x, world_y = pygame.mouse.get_pos()

            # Convert screen position to world position (if necessary)
            if not is_world_coordinates:  # Replace with a flag indicating world coordinates
                world_x -= scroll[0]  # Adjust based on scroll if needed
                world_y -= scroll[1]

            # Get player's current world position
            player_world_x, player_world_y = get_player_world_position(world_x, world_y, scroll)

            #print(f"World Click: ({world_x}, {world_y})")
            #print(f"Player World Position: ({player_world_x}, {player_world_y})")

            # Calculate animation position relative to player position
            animation_world_x = world_x + player_world_x
            animation_world_y = world_y + player_world_y

            # Append animation data with world position relative to player

            ActiveAnimations.append([0, [animation_world_x, animation_world_y], 5, 5, 60, "SHOT"])
            PlaySoundEffect(0)
            spawn_animation = True  # Set flag to True after spawning


    # Update and draw animations (unchanged from previous code)

    # Update and draw animations
    for animation in ActiveAnimations:
        animationIndex = animation[0]
        animationSpeed = animation[2]
        animationFrame = animation[3]
        animationTotalFrames = animation[4]
        world_position = animation[1]  # Access world position from data

        # Calculate screen position based on world position and scroll
        screen_position = [world_position[0] - scroll[0] - AnimationFrameList[animationIndex][(round(animationFrame/animationSpeed)-1)].get_width()/2, world_position[1] - scroll[1] - AnimationFrameList[animationIndex][(round(animationFrame/animationSpeed)-1)].get_height()/2]

        try:
            # Use screen position for blitting (considering scroll)
            pygame.Surface.blit(display, AnimationFrameList[animationIndex][(round(animationFrame/animationSpeed)-1)], screen_position)
        except IndexError as e:
            debug(f"Invalid Animation Time {(round(animationFrame/animationSpeed)-1)}", 3)

        
            
    
    for i in range(len(ActiveAnimations)):
        try:
            if ActiveAnimations[i][3] >= ActiveAnimations[i][4]:
                #print(f"Pop {i}, {ActiveAnimations[i][3]}, {(round(animationFrame/animationSpeed)-1)}")
                ActiveAnimations.pop(i)
            else:
                ActiveAnimations[i][3] += 1 / (FPS) * 60
        except IndexError as e:
            pass
                    #debug(f"Invalid Animation Time {(round(animationFrame/animationSpeed)-1)}", 3)
                    #pygame.quit()
        
        
     
    
    #pygame.Surface.blit(display, AnimationFrameList[1][0], (200,100))
    
    #pygame.Surface.blit(display, AnimationAssets[1], (200,100))
    
    
    if DEBUG:
        GUIdebug.NewFrame()
        GUIdebug.drawDebugText("DEBUG MENU", False)
        GUIdebug.drawDebugText(round(FPS), Text="FPS")
        GUIdebug.drawDebugText(objects)
        GUIdebug.drawDebugText(f"x: {round(scroll[0])} y:{round(scroll[1])}")
        GUIdebug.drawDebugText(f"{len(rockLock)}")
        GUIdebug.drawDebugText(f"{round(dt,5)}")
        GUIdebug.drawDebugText(f"{len(ActiveAnimations)}")
        GUIdebug.drawDebugText(f"Keys: {''.join(keysDown)}")
        
    if FPS < 25:
        GUIdebug.drawDebugText(f"LOW FPS")
    
    player.drawHP()
    
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick()
