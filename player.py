import pygame as pg
import math
import RPi.GPIO as GPIO
from mpu6050 import mpu6050 
from settings import *

buzzer_pin = 17
led1, led2 = 27, 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT) 
GPIO.setup(led1, GPIO.OUT) 
GPIO.setup(led2, GPIO.OUT) 
GPIO.setwarnings(False)

global Buzz 
Buzz = GPIO.PWM(buzzer_pin, 100) 

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Player(pg.sprite.Sprite):
    def __init__(self, app, name='car'):
        self.app = app
        self.group = app.main_group
        self.lap = -1
        self.is_crossing = False
        super().__init__(self.group)

        self.group.change_layer(self, CENTER.y)

        size = vec2([50, 50])
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect(center=CENTER)

        self.offset = vec2(0)
        self.inc = vec2(0)
        self.prev_inc = vec2(0)
        self.angle = 3.14/2
        self.diag_move_corr = 1 / math.sqrt(2)

        self.attrs = STACKED_SPRITE_ATTRS[name]
        self.cache = app.cache.stacked_sprite_cache
        self.viewing_angle = app.cache.viewing_angle
        self.rotated_sprites = self.cache[name]['rotated_sprites']
        
        self.name = ""
        self.mpu = None

    def setup_mpu(self):
        try:
            self.mpu = mpu6050(0x68)
        except Exception as e:
            print(f"{e}")
            self.mpu = None

    def set_name(self, name: str):
        self.name = name

    def control(self):
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)

        self.inc = vec2(0)
        speed = PLAYER_SPEED * self.app.delta_time
        rot_speed = PLAYER_ROT_SPEED * self.app.delta_time
        
        if self.mpu != None:
            accel_data = self.mpu.get_accel_data()
            accel_y = accel_data['y']
            rot_wheel = map_value(accel_y, -10, 10, -PLAYER_ROT_SPEED, PLAYER_ROT_SPEED) * self.app.delta_time
            self.angle += rot_wheel

        key_state = pg.key.get_pressed()
        
        if key_state[pg.K_LEFT]:
            self.angle += rot_speed
        if key_state[pg.K_RIGHT]:
            self.angle += -rot_speed
    
        if key_state[pg.K_w]:
            GPIO.output(led1, GPIO.HIGH)
            self.inc.x += speed * math.sin(self.angle * 2)
            self.inc.y += speed * math.cos(self.angle * 2)

        if key_state[pg.K_s]:
            GPIO.output(led2, GPIO.HIGH)
            self.inc.x -= speed * math.sin(self.angle * 2)
            self.inc.y -= speed * math.cos(self.angle * 2)

        if self.inc.x and self.inc.y:
            self.inc *= self.diag_move_corr


    def check_collision(self):
        hit = pg.sprite.spritecollide(self, self.app.collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask)
        if not hit:
            Buzz.stop()
            if self.inc.x or self.inc.y:
                self.prev_inc = self.inc
        else:
            Buzz.start(50) 
            self.inc = -self.prev_inc

        hit = pg.sprite.spritecollide(self, self.app.finishline_group,
                                      dokill=False, collided=pg.sprite.collide_mask)
        if hit:
            self.is_crossing = True

        if self.is_crossing == True and not hit:
            self.lap += 1
            print(self.lap)
            self.is_crossing = False

    def update(self):
        self.control()
        self.check_collision()
        self.get_image()
        self.move()
        self.app.server.update_pos(self.offset, self.angle)

    def move(self):
        self.offset += self.inc

    def get_image(self):
        frame = math.degrees(self.angle) % 360
        frame = int(frame / (360 / NUM_ANGLES))

        self.image = self.rotated_sprites[frame]
        self.rect = self.image.get_rect(center=self.rect.center)


