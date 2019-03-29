import game
import pygame
import random

'module with user interface'


class Game:
    def __init__(self):
        '''initializes faller and state'''
        self.running = True
        self.f = None
        self.faller = None



    def run(self) -> None:
        '''main user interface'''
        T = (127, 255, 212)
        R = (255,64,64)
        P = (255,20,147)
        Y = (255,215,0)
        G = (69,139,0)
        B = (100,149,237)
        L = ((191,62,255))

        grid = game.startgrid()
        g = game.GameState()
        f = self.randomfaller()
        self.f = f
        faller = game.Faller(f[0], grid, f[1], f[2], f[3], g)
        self.faller = faller
        pygame.init()
        self.resizesurface((750, 750))
        clock = pygame.time.Clock()

        t = 0
        while self.running:
            clock.tick(200)
            if self.faller.state == 'done':
                surface = pygame.display.get_surface()
                surface.fill(pygame.Color(0, 0, 0))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 100, 1, 1)
                textsurface = myfont.render('GAME OVER', True, (255, 215, 0))
                surface.blit(textsurface, (137, 205))
                pygame.display.flip()
            self.handle_events()
            if t%60 == 0:
                if self.faller.state == 'ready':
                    newgrid = self.faller.copy
                    f = self.randomfaller()
                    self.f = f
                    faller = game.Faller(f[0], newgrid, f[1], f[2], f[3], g)
                    self.faller = faller
                self.faller.tick()
                self.redraw(self.faller.copy)
            t = t + 1

        pygame.quit()

    def handle_events(self) -> None:
        '''handles events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.key_handle(event.key)

    def key_handle(self,key) -> None:
        '''handles key pressed events'''
        if key == pygame.K_SPACE:
            self.faller.rotate()
        elif key == pygame.K_RIGHT:
            self.faller.moveright()
        elif key == pygame.K_LEFT:
            self.faller.moveleft()

    def drawboard(self,grid) -> None:
        '''draws board & grid'''
        surface = pygame.display.get_surface()
        pygame.font.init()
        myfont = pygame.font.SysFont('Arial', 65,1,1)
        textsurface = myfont.render('C O L U M N S', True, (255,215,0))
        surface.blit(textsurface, (205, 50))

        yval = 100
        for a in grid:
            yval += 43
            xval = 200
            for c in a:
                xval += 43
                self.drawjewels(c,xval,yval)

    def redraw(self,grid) -> None:
        '''redraws surface'''
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(0, 0, 0))
        self.drawboard(grid)
        pygame.display.flip()


    def randomfaller(self) -> list:
        '''creates a random faller'''
        colors = ['T', 'R', 'P', 'Y', 'G', 'B', 'L']
        color1 = random.choice(colors)
        color2 = random.choice(colors)
        color3 = random.choice(colors)
        col = random.randint(1, 6)
        faller = [col, color1, color2, color3]
        return faller

    def drawjewels(self,str,xval,yval) -> None:
        '''draws jewels based on their state'''
        surface = pygame.display.get_surface()
        if '[' in str or (len(str) == 1 and str is not ' '):
            if 'T' in str:
                pygame.draw.rect(surface, (127, 255, 212), [xval, yval, 40, 40])
            elif 'R' in str:
                pygame.draw.rect(surface, (255, 64, 64), [xval, yval, 40, 40])
            elif 'P' in str:
                pygame.draw.rect(surface, (255, 20, 147), [xval, yval, 40, 40])
            elif 'Y' in str:
                pygame.draw.rect(surface, (255, 215, 0), [xval, yval, 40, 40])
            elif 'G' in str:
                pygame.draw.rect(surface, (69, 139, 0), [xval, yval, 40, 40])
            elif 'B' in str:
                pygame.draw.rect(surface, (100, 149, 237), [xval, yval, 40, 40])
            elif 'L' in str:
                pygame.draw.rect(surface, ((191, 62, 255)), [xval, yval, 40, 40])
        elif '|' in str:
            if 'T' in str:
                pygame.draw.rect(surface, (127, 255, 212), [xval, yval, 40, 40])
                pygame.draw.circle(surface, (0, 0, 0), [xval + 20, yval + 20], 6)
            elif 'R' in str:
                pygame.draw.rect(surface, (255, 64, 64), [xval, yval, 40, 40])
                pygame.draw.circle(surface, (0, 0, 0), [xval + 20, yval + 20], 6)
            elif 'P' in str:
                pygame.draw.rect(surface, (255, 20, 147), [xval, yval, 40, 40])
                pygame.draw.circle(surface, (0, 0, 0), [xval + 20, yval + 20], 6)
            elif 'Y' in str:
                pygame.draw.rect(surface, (255, 215, 0), [xval, yval, 40, 40])
                pygame.draw.circle(surface, (0, 0, 0), [xval + 20, yval + 20], 6)
            elif 'G' in str:
                pygame.draw.rect(surface, (69, 139, 0), [xval, yval, 40, 40])
                pygame.draw.circle(surface, (0, 0, 0), [xval + 20, yval + 20], 6)
            elif 'B' in str:
                pygame.draw.rect(surface, (100, 149, 237), [xval, yval, 40, 40])
                pygame.draw.circle(surface, (0, 0, 0), [xval + 20, yval + 20], 6)
            elif 'L' in str:
                pygame.draw.rect(surface, ((191, 62, 255)), [xval, yval, 40, 40])
                pygame.draw.circle(surface, (0, 0, 0), [xval + 20, yval + 20], 6)
        else:
            pygame.draw.rect(surface, (255, 255, 255), [xval, yval, 40, 40])


    def resizesurface(self, size: (int, int)) -> None:
        '''makes window resizable'''
        pygame.display.set_mode(size, pygame.RESIZABLE)



if __name__ == '__main__':
    Game().run()
