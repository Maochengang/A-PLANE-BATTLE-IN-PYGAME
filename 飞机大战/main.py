import pygame.sprite
import enemy
import myplane
import bullet
import supply
from random import *
from pygame.locals import *
from background import *

pygame.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战-----design by 吴泽琛")

# 加载声音
pygame.mixer.music.load("./sound/飞机大战.mp3")
pygame.mixer.music.set_volume(0.6)

bullet_sound = pygame.mixer.Sound("./sound/bullet.wav")
bullet_sound.set_volume(0.1)

supply_sound = pygame.mixer.Sound("./sound/supply.wav")
supply_sound.set_volume(0.2)

bomb_sound = pygame.mixer.Sound("./sound/use_bomb.wav")
bomb_sound.set_volume(0.2)

get_bullet_sound = pygame.mixer.Sound("./sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)

get_bomb_sound = pygame.mixer.Sound("./sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)

upgrade_sound = pygame.mixer.Sound("./sound/upgrade.wav")
upgrade_sound.set_volume(0.2)

enemy3_fly_sound = pygame.mixer.Sound("./sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound("./sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)

enemy2_down_sound = pygame.mixer.Sound("./sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)

enemy1_down_sound = pygame.mixer.Sound("./sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)

me_down_sound = pygame.mixer.Sound("./sound/me_down.wav")
me_down_sound.set_volume(0.2)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 创建滚动背景图像
bg1 = Background()
bg2 = Background(True)
bg_group = pygame.sprite.Group(bg1, bg2)

# 创建事件
SUPPLY_TIME = pygame.USEREVENT
DOUBLE_BULLET_TIME = pygame.USEREVENT + 1
INVINCIBLE_TIME = pygame.USEREVENT + 2

# 子弹数量
BULLET1_NUM = 4
BULLET2_NUM = 12


def inc_speed(target, inc):
    for e in target:
        e.speed += inc


def main():
    # 循环播放背景音乐
    pygame.mixer.music.play(-1)

    # 设置时钟来控制屏幕刷新频率
    clock = pygame.time.Clock()

    # 生成我放战机
    me = myplane.MyPlane(bg_size)

    # 生成敌方精灵组, 检测时只需将精灵组与me比较
    enemy_group = pygame.sprite.Group()

    # 生成小型敌机组
    small_enemies = pygame.sprite.Group()
    enemy.SmallEnemy.add_small_enemies(small_enemies, enemy_group, bg_size, 50)

    # 生成中型敌机组
    mid_enemies = pygame.sprite.Group()
    enemy.MidEnemy.add_mid_enemies(mid_enemies, enemy_group, bg_size, 6)

    # 生成大型敌机组
    big_enemies = pygame.sprite.Group()
    enemy.BigEnemy.add_big_enemies(big_enemies, enemy_group, bg_size, 4)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1((me.rect.centerx - 20, me.rect.centery)))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    for i in range(BULLET2_NUM // 3):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 30, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # 是否暂停游戏
    paused = False
    paused_nor_image = pygame.image.load("./images/pause_nor.png")
    paused_pressed_image = pygame.image.load("./images/pause_pressed.png")
    resume_nor_image = pygame.image.load("./images/resume_nor.png")
    resume_pressed_image = pygame.image.load("./images/resume_pressed.png")
    paused_image = paused_nor_image
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left = width - paused_rect.width - 10
    paused_rect.top = 10

    # 统计得分
    score = 0
    score_font = pygame.font.Font('./font/rough.ttf', 36)

    # 设置生命数量
    life_image = pygame.image.load("./images/life.png")
    life_rect = life_image.get_rect()
    life_num = 3

    # 设置游戏等级
    level = 1

    # 设置游戏运行变量
    running = True

    # 设置图像转换变量
    switch_image = False

    # 设置延迟变量
    delay = 100

    # 设置全屏炸弹
    bomb_image = pygame.image.load("./images/bomb.png")
    bomb_image_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("./font/font.ttf", 48)
    bomb_num = 3

    # 30秒生成一个补给包
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)  # 30 * 1000毫秒等于30秒

    # 是否使用超级子弹
    is_double_bullet = False

    # 中弹图片索引
    enemy1_destroy_index = 0
    enemy2_destroy_index = 0
    enemy3_destroy_index = 0
    me_destroy_index = 0

    # 用于阻止重复打开记录文件
    recorded = False

    # 游戏开始画面
    game_begin_font = pygame.font.Font("./font/font.ttf", 48)
    begin_image = pygame.image.load("./images/begin.png").convert_alpha()
    invincible_image = pygame.image.load("./images/invincible.png").convert_alpha()
    begin_image_rect = begin_image.get_rect()
    invincible_image_rect = invincible_image.get_rect()

    # 游戏结束画面
    game_over_font = pygame.font.Font("./font/font.ttf", 48)
    over_image = pygame.image.load("./images/game_over.png")
    again_image = pygame.image.load("./images/again.png")
    again_image_rect = again_image.get_rect()
    over_image_rect = over_image.get_rect()

    # 绘制背景图像
    bg_group.update()
    bg_group.draw(screen)

    # 是否进入无敌模式
    invincible = False

    # 是否进入超级战机模式
    super_me = True
    super_bullet = False

    # 是否退出选择页面
    out = False

    # 选择模式
    while True:
        bg_group.update()
        bg_group.draw(screen)
        # 绘制模式按钮
        begin_image_rect.left = (width - begin_image_rect.width) // 2
        begin_image_rect.top = (height - begin_image_rect.height) // 2
        invincible_image_rect.left = (width - invincible_image_rect.width) // 2
        invincible_image_rect.top = (height - invincible_image_rect.height) // 2 + 50
        screen.blit(begin_image, begin_image_rect)
        screen.blit(invincible_image, invincible_image_rect)
        clock.tick(60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # 正常模式
                    if begin_image_rect.left < event.pos[0] < begin_image_rect.right and \
                            begin_image_rect.top < event.pos[1] < begin_image_rect.bottom:
                        invincible = False
                        out = True
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        break
                    # 无敌模式，此模式下战机无敌，补给10秒一个,无限炸药包
                    if invincible_image_rect.left < event.pos[0] < invincible_image_rect.right and \
                            invincible_image_rect.top < event.pos[1] < invincible_image_rect.bottom:
                        invincible = True
                        out = True
                        pygame.time.set_timer(SUPPLY_TIME, 10 * 1000)
                        life_num = 1
                        break
        if out:
            break

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = paused_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bomb_num > 0:
                        bomb_sound.play()
                        if not invincible:
                            bomb_num -= 1
                        for e in enemy_group:
                            if e.rect.bottom > 0:
                                e.active = False
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        if level == 1 and score > 180000:
            level = 2
            upgrade_sound.play()
            enemy.SmallEnemy.add_small_enemies(small_enemies, enemy_group, bg_size, 5)
            enemy.MidEnemy.add_mid_enemies(mid_enemies, enemy_group, bg_size, 2)
            enemy.BigEnemy.add_big_enemies(big_enemies, enemy_group, bg_size, 1)
            inc_speed(small_enemies, 1)

        if level == 2 and score > 360000:
            level = 3
            upgrade_sound.play()
            enemy.SmallEnemy.add_small_enemies(small_enemies, enemy_group, bg_size, 5)
            enemy.MidEnemy.add_mid_enemies(mid_enemies, enemy_group, bg_size, 1)
            enemy.BigEnemy.add_big_enemies(big_enemies, enemy_group, bg_size, 1)
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)

        # 战机升级， 子弹四倍伤害，移动速度提升二倍
        if level == 3 and score > 800000 and super_me:
            level = 4
            upgrade_sound.play()
            super_me = False
            super_bullet = True
            upgrade_sound.play()
            me.change_face(bg_size)
            enemy.SmallEnemy.add_small_enemies(small_enemies, enemy_group, bg_size, 5)
            enemy.MidEnemy.add_mid_enemies(mid_enemies, enemy_group, bg_size, 1)
            enemy.BigEnemy.add_big_enemies(big_enemies, enemy_group, bg_size, 1)
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)

        if level == 4 and score > 1200000:
            level = 5
            upgrade_sound.play()
            enemy.SmallEnemy.add_small_enemies(small_enemies, enemy_group, bg_size, 1)
            enemy.MidEnemy.add_mid_enemies(mid_enemies, enemy_group, bg_size, 2)
            enemy.BigEnemy.add_big_enemies(big_enemies, enemy_group, bg_size, 1)
            # 提升小型敌机速度
            inc_speed(small_enemies, 0.1)
            # 提升中型敌机速度
            inc_speed(mid_enemies, 0.1)
            # 提升大型敌机速度
            inc_speed(big_enemies, 0.5)

        if level == 5 and score > 2000000:
            level = 6
            upgrade_sound.play()
            enemy.SmallEnemy.add_small_enemies(small_enemies, enemy_group, bg_size, 1)
            enemy.MidEnemy.add_mid_enemies(mid_enemies, enemy_group, bg_size, 1)
            enemy.BigEnemy.add_big_enemies(big_enemies, enemy_group, bg_size, 1)
            # 提升小型敌机速度
            inc_speed(small_enemies, 0.1)
            # 提升中型敌机速度
            inc_speed(mid_enemies, 0.1)
            # 提升大型敌机速度
            inc_speed(big_enemies, 0.1)

        if level == 6 and score > 3000000:
            level = 7
            upgrade_sound.play()
            enemy.SmallEnemy.add_small_enemies(small_enemies, enemy_group, bg_size, 1)
            enemy.MidEnemy.add_mid_enemies(mid_enemies, enemy_group, bg_size, 1)
            enemy.BigEnemy.add_big_enemies(big_enemies, enemy_group, bg_size, 1)
            # 提升小型敌机速度
            inc_speed(small_enemies, 0.1)
            # 提升中型敌机速度
            inc_speed(mid_enemies, 0.1)
            # 提升大型敌机速度
            inc_speed(big_enemies, 0.1)

        # 绘制背景图像
        bg_group.update()
        bg_group.draw(screen)

        # 没有暂停并且战机生命大于0
        if life_num and not paused:
            # 检测用户键盘是否按下
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                me.move_up()
            if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                me.move_down()
            if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                me.move_left()
            if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                me.move_right()

            # 绘制全屏炸弹
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num + 1
                    bomb_supply.active = False

            # 绘制超级子弹
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                # 检测战机是否获得超级子弹
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # 发射子弹
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 20, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx - 60, me.rect.centery))
                    bullets[bullet2_index + 2].reset((me.rect.centerx + 20, me.rect.centery))
                    bullet2_index = (bullet2_index + 3) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset((me.rect.centerx - 17.5, me.rect.centery))
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否与敌机相撞
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemy_group, False, pygame.sprite.collide_mask)
                    if enemies_hit:
                        b.active = False
                        for e in enemies_hit:
                            if e in mid_enemies or e in big_enemies:
                                if super_bullet:
                                    e.energy -= 4
                                else:
                                    e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (delay % 3):
                        if enemy1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[enemy1_destroy_index], each.rect)
                        enemy1_destroy_index = (enemy1_destroy_index + 1) % 4
                        if enemy1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:  # 被打时触发打击特效
                        screen.blit(each.hit_image, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    # 绘制血槽
                    pygame.draw.line(screen,
                                     BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.3:
                        line_color = GREEN
                    else:
                        line_color = RED
                    pygame.draw.line(screen,
                                     line_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)
                else:
                    if not (delay % 3):
                        if enemy2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[enemy2_destroy_index], each.rect)
                        enemy2_destroy_index = (enemy2_destroy_index + 1) % 4
                        if enemy2_destroy_index == 0:
                            score += 4000
                            each.reset()

            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:  # 被打时触发打击特效
                        screen.blit(each.hit_image, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    # 绘制血槽
                    pygame.draw.line(screen,
                                     BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.4:
                        line_color = GREEN
                    else:
                        line_color = RED
                    pygame.draw.line(screen,
                                     line_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)
                    if each.rect.bottom - 50 > 0:
                        enemy3_fly_sound.play()
                else:  # 毁灭
                    if not (delay % 3):
                        if enemy3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[enemy3_destroy_index], each.rect)
                        enemy3_destroy_index = (enemy3_destroy_index + 1) % 6
                        if enemy3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            # 检测我放战机是否与敌方战机相撞，相撞则返回列表
            enemies_down = pygame.sprite.spritecollide(me, enemy_group, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                if not invincible:
                    me.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制动态战机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制战机生命数量
            if life_num:
                for life in range(life_num):
                    screen.blit(life_image, (width - 10 - (life + 1) * life_rect.width, height - 10 - life_rect.height))

            # 绘制全屏炸弹
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_image_rect.height))
            screen.blit(bomb_text, (20 + bomb_image_rect.width, height - 10 - bomb_image_rect.height))

            # 绘制分数
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

        # 游戏结束画面
        elif life_num == 0:
            # 结束背景音乐
            pygame.mixer.music.stop()

            # 停止全部音效
            pygame.mixer.stop()

            # 停止补给发放
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not recorded:
                recorded = True

                # 读取历史最高得分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())

                # 如果玩家得分高于最高分则存档
                if score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))
            # 绘制历史最高分
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            # 绘制本次游戏分数
            game_over_text1 = game_over_font.render("Your Score", True, (255, 255, 255))
            game_over_text1_rect = game_over_text1.get_rect()
            game_over_text1_rect.left = (width - game_over_text1_rect.width) // 2
            game_over_text1_rect.top = height // 3
            screen.blit(game_over_text1, game_over_text1_rect)
            game_over_text2 = game_over_font.render(str(score), True, (255, 255, 255))
            game_over_text2_rect = game_over_text2.get_rect()
            game_over_text2_rect.left = (width - game_over_text2_rect.width) // 2
            game_over_text2_rect.top = game_over_text1_rect.top + 70
            screen.blit(game_over_text2, game_over_text2_rect)

            # 绘制重新开始
            again_image_rect.left = (width - again_image_rect.width) // 2
            again_image_rect.top = game_over_text2_rect.bottom + 50
            screen.blit(again_image, again_image_rect)

            # 绘制结束游戏
            over_image_rect.left = (width - over_image_rect.width) // 2
            over_image_rect.top = again_image_rect.bottom + 50
            screen.blit(over_image, over_image_rect)

            # 检测鼠标左键是否按下
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_image_rect.left < pos[0] < again_image_rect.right and \
                        again_image_rect.top < pos[1] < again_image_rect.bottom:
                    # 重新开始游戏
                    main()
                if over_image_rect.left < pos[0] < over_image_rect.right and \
                        over_image_rect.top < pos[1] < over_image_rect.bottom:
                    # 退出游戏
                    pygame.quit()
            # pygame.quit()

        # 绘制暂停图像
        screen.blit(paused_image, paused_rect)

        # 限制绘图时间，优化突突突的效果
        if not (delay % 3):
            switch_image = not switch_image
        if delay:
            delay -= 1
        else:
            delay = 100

        # 刷新图像
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    # try:
    #     main()
    # except SystemExit:  # 如果异常是系统退出则略过
    #     pass
    # except:
    #     traceback.print_exc()
    main()
    pygame.quit()
    input()  # 此处接收用户输入才能往下走
