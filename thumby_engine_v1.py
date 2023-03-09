import time
import thumby
import math

# BITMAP: width: 32, height: 32
bitmap0 = bytearray([0,0,0,0,0,0,0,0,248,8,232,40,40,40,40,40,40,40,40,40,40,232,8,248,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,255,0,63,32,32,32,32,32,32,32,32,32,32,63,0,255,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,255,0,12,12,63,63,12,12,0,0,24,24,3,3,0,255,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,31,16,16,16,16,20,18,16,20,18,16,16,16,16,16,31,0,0,0,0,0,0,0,0])

class Level:
    # ref to engine
    def update(self):
        pass
    

class Anchor:
    pos_x: int
    pos_y: int
    x_delta: int
    y_delta: int
    sprite: thumbySprite

    def __init__(self, _sprite):
        self.sprite = _sprite
        self.pos_x = _sprite.x
        self.pos_y = _sprite.y
    
    def update(self):
        self.x_delta = self.sprite.x - self.pos_x
        self.y_delta = self.sprite.y - self.pos_y
        self.pos_x = self.sprite.x
        self.pos_y = self.sprite.y


class RenderManager:
    Sprites: list
    Text: string
    x_delta: int
    y_delta: int
    anchor: Entity
    x_center: int
    y_center: int
    text_x: int
    text_y: int
    
    def __init__(self):
        self.Sprites = []
        self.Text = ""
        self.x_center = int(thumby.display.width/2)
        self.y_center = int(thumby.display.height/2)
        self.text_x = self.x_center
        self.text_y = self.y_center
    
    def render(self):
        
        if self.anchor is not None:
            self.x_delta = -self.anchor.x_delta
            self.y_delta = -self.anchor.y_delta
            
        for i in self.Sprites:
            if self.anchor is not None and self.anchor.sprite == i:
                i.x = int(self.x_center - (32/2))
                i.y = int(self.y_center - (32/2))
            else:
                i.x += self.x_delta
                i.y += self.y_delta
            thumby.display.drawSprite(i)
        
        if self.Text != "":
            thumby.display.drawText(self.Text, self.text_x, self.text_y, 1)
        
        thumby.display.update()
    
    def add_sprite(self, sprite):
        self.Sprites.append(sprite)
    
    def clear_sprites(self):
        self.Sprites.clear()
    
    def set_text(self, _text):
        self.Text = _text
       
    def center_text(self):
        self.text_x = self.x_center
        self.text_y = self.y_center
        
    def set_text_loc(self, x: int, y: int):
        self.text_x = x
        self.text_y = y
     
    def set_anchor(self, _anchor):
        self.anchor = _anchor


class ThumbyEngine:
    done: bool
    visuals: RenderManager
    level: Level
    anchor: Entity

    def __init__(self):
        thumby.display.setFPS(60)
        self.done = False
        self.visuals = RenderManager()
    
    def run(self):
        while not self.done:
            self.level.update()
            self.visuals.render()
    
    def set_level(self, _level):
        self.visuals.clear_sprites()
        self.level = _level
        self.level.init(self)
        
    def set_FPS(self, _target: int):
        thumby.display.setFPS(_target)


class SimpleLevel(Level):
    
    mySprite: thumbySprite
    engine: ThumbyEngine
    lvlAnchor: Anchor
    
    def init(self, _engine):
        self.engine = _engine
        
        # Make a sprite object using bytearray (a path to binary file from 'IMPORT SPRITE' is also valid)
        self.mySprite = thumby.Sprite(32, 32, bitmap0)
        self.mySprite.x = int((thumby.display.width/2) - (32/2))
        self.engine.visuals.add_sprite(self.mySprite)
        
        # Example of setting a camera anchor
        self.lvlAnchor = Anchor(self.mySprite)
        self.engine.visuals.set_anchor(self.lvlAnchor)
        
        # Creating a second sprite in the level
        self.secondSprite = thumby.Sprite(15, 15, bitmap0, 0, 0)
        self.engine.visuals.add_sprite(self.secondSprite)
    
    # Called once every frame
    def update(self):
        t0 = time.ticks_ms()   # Get time (ms)
        thumby.display.fill(0) # Fill canvas to black
    
        bobRate = 250 # Set arbitrary bob rate (higher is slower)
        bobRange = 5  # How many pixels to move the sprite up/down (-5px ~ 5px)
    
        # Calculate number of pixels to offset sprite for bob animation
        bobOffset = math.sin(t0 / bobRate) * bobRange
    
        # Apply bob offset
        self.mySprite.y = int(round((thumby.display.height/2) - (32/2) + bobOffset))
        
        self.lvlAnchor.update()


def test_main():
    e = ThumbyEngine()
    l = SimpleLevel()
    e.set_level(l)
    e.run()


test_main()
