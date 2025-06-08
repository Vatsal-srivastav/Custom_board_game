import pygame
import zipfile
import io

GREEN = (0, 128, 0)
WHITE = (255, 255, 255)

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

GRID_SIZE = 9
SQUARE_SIZE = WINDOW_WIDTH // GRID_SIZE            

def game_over(game_over_text, screen):
    font = pygame.font.SysFont("Impact", 72)
    text = font.render(game_over_text, True, (0, 0, 0))
    text_rect = text.get_rect(center=(WINDOW_WIDTH//2,WINDOW_WIDTH-SQUARE_SIZE//4))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(WHITE)
        screen.blit(text, text_rect)
        pygame.display.flip()        
                    

def move_piece(mousepos, moving_piece,board):
    ox=moving_piece[0]//SQUARE_SIZE
    oy=moving_piece[1]//SQUARE_SIZE
    nx=mousepos[0]//SQUARE_SIZE
    ny=mousepos[1]//SQUARE_SIZE
    board=update_piece(ox,oy,nx,ny,board)
    return board

def update_piece(ox,oy,nx,ny,board):
    if board[nx][ny]==0 or (board[nx][ny].status!='Castle' and board[nx][ny].status!='CC'):
      if board[ox][oy].status!="CC":   
        board[nx][ny]=board[ox][oy]
        board[ox][oy]=0        
        return board  
      else:
        board[nx][ny]=board[ox][oy].capturer
        board[ox][oy]=Castle()        
        return board 
    else:
        board[nx][ny]=CapturedCastle(board[ox][oy])
        board[ox][oy]=0        
        return board          
        
def find_moves(board,p):
    x=p[0]//SQUARE_SIZE
    y=p[1]//SQUARE_SIZE
    piece=board.board[x][y]
    m=piece.get_moves(x,y,board.board)
    return m

def draw_moves(moves,screen):
    for i in moves:
        center=((i[0]*SQUARE_SIZE)+SQUARE_SIZE//2,(i[1]*SQUARE_SIZE)+SQUARE_SIZE//2)
        pygame.draw.circle(screen, (0, 178, 0),center, SQUARE_SIZE//5)

def check_validity(p,board,current_turn):
    x=p[0]//SQUARE_SIZE
    y=p[1]//SQUARE_SIZE
    piece=board.board[x][y]
    if (piece!=0) and (piece.side==current_turn):
        return True
    else:
        return False    
    
class Castle:
    def __init__(self):
        self.status='Castle'
        self.side='a'
        with zipfile.ZipFile('pieces_image.zip') as zf:
            with zf.open('castle.png') as file:
                CASTLE = file.read()
        self.image=pygame.image.load(io.BytesIO(CASTLE)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(SQUARE_SIZE,SQUARE_SIZE))
        self.image.set_colorkey(self.image.get_at((0, 0)))        

class CapturedCastle:
    def __init__(self,capturer):
        self.capturer=capturer
        self.side=capturer.side
        self.status='CC'
        with zipfile.ZipFile('pieces_image.zip') as zf:
            with zf.open('castle.png') as file:
                CASTLE = file.read()
        self.image1=pygame.image.load(io.BytesIO(CASTLE)).convert_alpha()
        self.image1= pygame.transform.scale(self.image1,(SQUARE_SIZE,SQUARE_SIZE))
        self.image1.set_colorkey(self.image1.get_at((0, 0)))
        self.image2=capturer.image
        self.image2= pygame.transform.scale(self.image2,(SQUARE_SIZE//2,SQUARE_SIZE//2))
     
    def get_moves(self,x,y,board):
         return self.capturer.get_moves(x,y,board)
    
    def draw(self,x,y,screen):
         screen.blit(self.image1,(x,y))
         screen.blit(self.image2,(x+SQUARE_SIZE//2,y+SQUARE_SIZE//2))
                  
class Spartan:
    def __init__(self,side):
        self.side=side
        self.status='Spartan'
        with zipfile.ZipFile('pieces_image.zip') as zf:
            with zf.open('spartan.png') as file:
                CASTLE = file.read()
        self.image=pygame.image.load(io.BytesIO(CASTLE)).convert_alpha()        
        self.image= pygame.transform.scale(self.image,(SQUARE_SIZE,SQUARE_SIZE))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        if side=='v':
            self.image = pygame.transform.rotate(self.image, 180)
    
    def get_moves(self,x,y,board):
         m=[]
         for i in range(1,3):
             if (x+i)>=len(board):
                 break
             if board[x+i][y]==0:
                 m.append((x+i,y))
             elif board[x+i][y].side!=self.side:
                 m.append((x+i,y))
                 break 
             else:
                break
          
         for i in range(1,3):
             if (x-i)>=len(board):
                 break
             if board[x-i][y]==0:
                 m.append((x-i,y))
             elif board[x-i][y].side!=self.side:
                 m.append((x-i,y))
                 break 
             else:
                break
         
         for i in range(1,3):
             if (y+i)>=len(board[x]):
                 break
             if board[x][y+i]==0:
                 m.append((x,y+i))
             elif board[x][y+i].side!=self.side:
                 m.append((x,y+i))
                 break 
             else:
                break                            
           
         for i in range(1,3):
             if (y-i)>=len(board[x]):
                 break
             if board[x][y-i]==0:
                 m.append((x,y-i))
             elif board[x][y-i].side!=self.side:
                 m.append((x,y-i))
                 break 
             else:
                break     
         return m                                  

class Samurai:
    def __init__(self,side):
        self.side=side
        self.status='Samurai'
        with zipfile.ZipFile('pieces_image.zip') as zf:
            with zf.open('samurai.png') as file:
                CASTLE = file.read()
        self.image=pygame.image.load(io.BytesIO(CASTLE)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(SQUARE_SIZE,SQUARE_SIZE))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        if side=='v':
            self.image = pygame.transform.rotate(self.image, 180)
    
    def get_moves(self,x,y,board):
         m=[]
         for i in range(1,3):
             if (x+i)>=len(board) or (y+i)>=len(board):
                 break
             if board[x+i][y+i]==0:
                 m.append((x+i,y+i))
             elif board[x+i][y+i].side!=self.side:
                 m.append((x+i,y+i))
                 break 
             else:
                break
          
         for i in range(1,3):
             if (x-i)>=len(board) or (y-i)>=len(board):
                 break
             if board[x-i][y-i]==0:
                 m.append((x-i,y-i))
             elif board[x-i][y-i].side!=self.side:
                 m.append((x-i,y-i))
                 break 
             else:
                break
         
         for i in range(1,3):
             if (x+i)>=len(board) or (y-i)>=len(board):
                 break
             if board[x+i][y-i]==0:
                 m.append((x+i,y-i))
             elif board[x+i][y-i].side!=self.side:
                 m.append((x+i,y-i))
                 break 
             else:
                break                           
           
         for i in range(1,3):
             if (x-i)>=len(board) or (y+i)>=len(board):
                 break
             if board[x-i][y+i]==0:
                 m.append((x-i,y+i))
             elif board[x-i][y+i].side!=self.side:
                 m.append((x-i,y+i))
                 break 
             else:
                break     
         return m
            
class Crusader:
    def __init__(self,side):
        self.side=side
        self.status='Crusader'
        with zipfile.ZipFile('pieces_image.zip') as zf:
            with zf.open('crusader.png') as file:
                CASTLE = file.read()
        self.image=pygame.image.load(io.BytesIO(CASTLE)).convert_alpha()        
        self.image= pygame.transform.scale(self.image,(SQUARE_SIZE,SQUARE_SIZE))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        if side=='v':
            self.image = pygame.transform.rotate(self.image, 180)    
    
    def get_moves(self, x, y, board):
        moves = []
        possible_moves = [
            (x - 2, y - 1),
            (x - 2, y + 1),
            (x - 1, y - 2),
            (x - 1, y + 2),
            (x + 1, y - 2),
            (x + 1, y + 2),
            (x + 2, y - 1),
            (x + 2, y + 1),
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x + 1, y + 1),
            (x + 0, y + 1),
            (x + 0, y  - 1),
            (x + 1, y + 0),
            (x - 1, y + 0),
        ]
        
        for move in possible_moves:
            new_x, new_y = move
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                piece = board[new_x][new_y]
                if piece == 0 or piece.side != self.side:
                    moves.append(move)
        
        return moves  


class Board:
    def __init__(self,l):
        self.board=l
        self.depth=0
    
    def check_winner(self, board):
        v = 0
        p = 0
        for x in board:
            for y in x:
                if y != 0 and y.status == 'CC':
                    if y.side == 'v':
                        v += 1
                    if y.side == 'p':
                        p += 1
        if p == 3:
            return 'p'
        if v == 3:
            return 'v'
        return None

    def evaluate(board):
        evaluation = 0
        for piece in board:
            if piece != 0 and piece.side == 'v':
                evaluation += piece.value
            if piece != 0 and piece.side == 'p':
                evaluation -= piece.value
        return evaluation
              
    def reset(self):
        self.board[8][0]=Castle()
        self.board[4][4]=Castle()
        self.board[0][8]=Castle()
        
        self.board[0][0]=Crusader('v')
        self.board[8][8]=Crusader('p')
        
        self.board[0][1]=Spartan('v')
        self.board[1][1]=Spartan('v')
        self.board[1][0]=Spartan('v')
        
        self.board[1][2]=Samurai('v')
        self.board[2][2]=Samurai('v')
        self.board[2][1]=Samurai('v')
        
        self.board[7][8]=Spartan('p')
        self.board[7][7]=Spartan('p')
        self.board[8][7]=Spartan('p')
                
        self.board[7][6]=Samurai('p')
        self.board[6][6]=Samurai('p')
        self.board[6][7]=Samurai('p')
        
    def draw_board(self,screen):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row + col) % 2 == 0:
                    color = GREEN
                else:
                    color = WHITE
                
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                
                pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        self.draw_pieces(screen)
    
    def draw_pieces(self,screen):    
          for x in range(len(self.board)):
             for y in range(len(self.board[x])):
               if self.board[x][y]!=0:
                 if self.board[x][y].status!='CC':   
                   screen.blit(self.board[x][y].image,(x*SQUARE_SIZE,y*SQUARE_SIZE))
                 else:
                      self.board[x][y].draw(x*SQUARE_SIZE,y*SQUARE_SIZE,screen)
                      
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chessboard")

l1=[]
for x in range(9):
    l2=[]
    for y in range(9):
        l2.append(0)
    l1.append(l2)    
        
board=Board(l1)
board.reset()
players=('p','v')
current_turn='p'
addon=1
index=0
is_moving=False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.MOUSEBUTTONDOWN:
               if is_moving==False:
                   mouse_pos = pygame.mouse.get_pos()
                   v=check_validity(mouse_pos,board, current_turn)    
                   if v==True:
                       moves=find_moves(board,mouse_pos)
                       if moves!=[]:
                           moving_piece=mouse_pos
                           is_moving=True

               elif is_moving==True:
                    mouse_pos = pygame.mouse.get_pos()
                    if (mouse_pos[0]//SQUARE_SIZE,mouse_pos[1]//SQUARE_SIZE) in moves:
                        board.board=move_piece(mouse_pos,moving_piece,board.board)
                        index=index+addon
                        current_turn=players[index]
                        addon*=-1
                        winner=board.check_winner(board.board)
                        if winner=='p':
                            game_over('you won', screen)
                        if winner=='v':
                            game_over('you lost', screen)   
                    is_moving=False
                    moves=[]
                                         
       
    screen.fill(WHITE)
    
    board.draw_board(screen)    
    
    if is_moving==True:
        draw_moves(moves,screen)
    
    pygame.display.flip()

pygame.quit()
