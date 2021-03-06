''' Nado 게임 '''
import pygame
import random
import os

''' 게임 필수 세팅 '''
class NadoGame:
    pygame.init()
    pygame.display.set_caption("Nado Pang")
    # 화면 설정
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode(
        (screen_width, screen_height)
    )
    clock = pygame.time.Clock()

    def __init__(self):
        # 배경 및 stage 설정
        self.background = pygame.image.load("./image/background_1.png")
        self.stage = pygame.image.load("./image/stage.png")
        self.stage_size = self.stage.get_rect().size
        self.stage_height = self.stage_size[1]
        # 게임 총 시간 및 폰트 설정
        self.total_time = 150		  
        self.game_font = pygame.font.Font(None, 40)
    
    def drawing(self):
        # 배경 그리기
        self.screen.blit(self.background, (0,0) ) # OR &screen.fill((122,10,122))
        
        # 무기 그리기
        for x_pos, y_pos in Weapon.weapons:
            self.screen.blit(Weapon.image, (x_pos, y_pos) )
        
        # stage 그리기
        self.screen.blit(self.stage, (0 , self.screen_height - self.stage_height) )
        
        # 캐릭터 그리기
        for character in Character.character:
            self.screen.blit(character.image, (character.x_pos, character.y_pos) )
        
        # 공 그리기
        for ball in Ball.balls:
            self.screen.blit(ball.image, (ball.x_pos, ball.y_pos) )

        # 필수
        pygame.display.update()

    def update_before_drawing(self):
        # fps별 속도 보정
        dt = self.clock.tick(60)

        ''' 캐릭터 위치 정보 업데이트 '''
        character = Character.character[0]
        character.x_pos += character.to_x * dt
        # 화면 벗어남 방지
        if character.x_pos < 0:
            character.x_pos = 0
        elif character.x_pos > self.screen_width - character.width:
            character.x_pos = self.screen_width - character.width

        ''' 무기 정보 업데이트 '''
        # 무기가 위로 날라감				# w[1] --> weapon_y_pos
        Weapon.weapons = [ [w[0], w[1] - Weapon.speed * dt] for w in Weapon.weapons ]
        # 무기가 천장에 닿으면 사라짐		# 조건에 맞는 것만 저장한다.
        Weapon.weapons = [ [w[0], w[1]] for w in Weapon.weapons if w[1]>0]
        
        ''' 공 정보 '''
        # enumerate : 몇 번째 인덱스인지도 알려준다
        for ball_idx, ball in enumerate(Ball.balls):
            # 왼쪽, 오른쪽 벽에 부딪히는 경우
            if ball.x_pos <= 0 or ball.x_pos > nadoGame.screen_width - ball.width:
                ball.to_x = ball.to_x * -1    

            # 바닥에 부딪히는 경우
            if ball.y_pos > nadoGame.screen_height - nadoGame.stage_height - ball.height:
                ball.to_y = ball.ball_speed_y[0]
            # 그렇지 않은 경우 올라가면서 속도 감소, 내려가면서 속도 증가
            else:
                ball.to_y += 0.05

            ball.x_pos += ball.to_x * dt
            ball.y_pos += ball.to_y * dt


class Unit:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)	# 이미지 경로
        self.size = self.image.get_rect().size		# 이미지 크기
        self.width = self.size[0]					# 이미지 너비
        self.height = self.size[1]					# 이미지 높이

class Character(Unit):
    character = list()
    def __init__(self, image_path):
        # 이미지 설정
        Unit.__init__(self, image_path)
        # 시작위치 설정
        self.x_pos = nadoGame.screen_width/2 - self.width/2
        self.y_pos = nadoGame.screen_height - self.height - nadoGame.stage_height
        # 움직임 설정 변수
        self.to_x = 0
        self.speed = 0.5

        self.character.append(self)

    def rect(self):
        rect = self.image.get_rect()
        rect.left = self.x_pos
        rect.top =  self.y_pos
        return rect
    


class Ball(Unit):
    balls = list()
    # 공은 종류가 4개
    ball_speed_y = [-1.5, -1.2, -.9, -.6]
    ball_images=[
        "./image/balloon1.png",
        "./image/balloon2.png",
        "./image/balloon3.png",
        "./image/balloon4.png",
    ]
    def __init__(self, dict):
        img_idx = dict["img_idx"]
        image_path = self.ball_images[img_idx]
        Unit.__init__(self, image_path)

        self.x_pos = dict["x_pos"]
        self.y_pos = dict["y_pos"]
        self.to_x = dict["to_x"]
        self.to_y = dict["to_y"]

        self.balls.append(self)

    def rect(self):
        rect = self.image.get_rect()
        rect.left = self.x_pos
        rect.top = self.y_pos
        return rect

class Weapon:
    weapons = list()

    image = pygame.image.load("./image/weapon.png")
    size = image.get_rect().size
    width = size[0]
    height = size[1]
    speed = 0.3
    shot = 0

    @classmethod
    def append(cls, x_pos, y_pos):
        cls.weapons.append([x_pos, y_pos])
        cls.shot += 1
    
    @classmethod
    def rect(cls, idx):
        rect = cls.image.get_rect()
        rect.left = cls.weapons[idx][0]
        rect.top = cls.weapons[idx][1] + 25 # 공과 부딪히는 이벤트 시각적 보정
        return rect


 
print(dir(Weapon))
print(Weapon.__dict__)

# 이 게임의 정보 객체 생성
nadoGame = NadoGame()
# 주인공 캐릭터 생성, 객체 생성 함수와 통일을 맞춤
Character("./image/character.png")
character = Character.character[0]
# 최초 발생 큰공
Ball(
    {
        "x_pos" : 50,       # 공의 x좌표
        "y_pos" : 50,       # 공의 y좌표
        "img_idx" : 0,      # 공의 이미지 인덱스
        "to_x" : .2,
        "to_y" : .2,
    }
)


''' 게임 실행 '''
running = True                          # 게임 탈락 여부
stop = False
start_ticks = pygame.time.get_ticks()   # 시작 시간
kdown_right = False
kdown_left = False
weapon_to_remove = -1
ball_to_remove = -1

while running :

    ''' drawing '''
    nadoGame.drawing()
    if stop==True:
        running = False
        continue


    ''' event 처리 '''
    for event in pygame.event.get():
        # 창이 닫히는 이벤트가 발생
        if event.type == pygame.QUIT:
            running = False
            break
        
        # key down, char_pos setting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:         # 좌이동
                kdown_left = True
                #kdown_right = False
                character.to_x = -character.speed
            elif event.key == pygame.K_RIGHT:      # 우이동
                kdown_right = True
                #kdown_left = False
                character.to_x = +character.speed
            elif event.key == pygame.K_SPACE:      # space
                weapon_x_pos = character.x_pos + character.width/2 - Weapon.width / 2
                weapon_y_pos = character.y_pos
                Weapon.append(weapon_x_pos, weapon_y_pos)
        # key up, setting flag
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                kdown_left = False
            elif event.key == pygame.K_RIGHT:
                kdown_right = False
        
        # char_pos setting with flag, 기존 코드 개선 부분
        if (kdown_left == False) and (kdown_right == False):
            character.to_x = 0
        elif (kdown_left == False) and (kdown_right == True):
            character.to_x = character.speed
        elif (kdown_left == True) and (kdown_right == False):
            character.to_x = -character.speed
        
    ''' 이벤트 발생에 따른 이미지들 위치 정보 수정 '''
    nadoGame.update_before_drawing()

    ''' 특정 이벤트 처리 '''
    character_rect = character.rect()
    for ball_idx, ball in enumerate(Ball.balls):
        ball_rect = ball.rect()
        
        # 공이 캐릭터와 부딪힘?
        if character_rect.colliderect(ball_rect):
            stop = True
            continue

        # 공이 여러 무기들 중 한 무기와 부딪힘?
        for weapon_idx, weapon in enumerate(Weapon.weapons):
            weapon_rect = Weapon.rect(weapon_idx)
            if weapon_rect.colliderect(ball_rect):
                weapon_to_reomve = weapon_idx
                ball_to_remove = ball_idx

        # 부딪힌 무기와 공 삭제
        if ball_to_remove > -1:
            del Ball.balls[ball_to_remove]
            del Weapon.weapons[weapon_to_reomve]
            ball_to_remove = weapon_to_remove = -1
    
   
''' 게임 종료 '''
pygame.time.delay(200)
pygame.quit()
