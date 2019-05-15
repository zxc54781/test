import pygame
class Ficha:
    def __init__(self, Color):
        self.color = Color
        if self.color == "Naranja":
            self.image = pygame.image.load("./Imagenes/Ficha_Naranja.png")
        else:
            self.image = pygame.image.load("./Imagenes/Ficha_Azul.png")
        self.position = None
        self.queen_status = False

    @staticmethod
    def True_position(Xposition, Yposition, Squares):  # Aqui se da la posicion mas acertada en el cuadro
        position = (Xposition, Yposition)
        if position in Squares:
            return position
        for Square in Squares:
            for X in range(Xposition - 75, Xposition):
                if X == Square[0]:
                    for Y in range(Yposition - 75, Yposition):
                        if Y == Square[1]:
                            Real_position = Square
                            return Real_position


    @staticmethod
    # Esta funcion toma una posicion y checkea si en la lista hay una reina retornara Verdadero
    def Checking_The_Queens(Click_pos, Players1, Players2, Turn_Player):
        if Turn_Player == 1:
            for players in Players1:
                if players.position == Click_pos:
                    if players.queen_status:
                        return True
        else:
            for players2 in Players2:
                if players2.position == Click_pos:
                    if players2.queen_status:
                        return True

    @staticmethod
    def Find_Path2(D_Path1, D_Path2, Eat_Path1, Eat_Path2, Player1, Player2):
        Ocuped_Epath1, Ocuped_Epath2 = None, None
        if Eat_Path1 == 1:
            Ocuped_Epath1 = True
        if Eat_Path2 == 1:
            Ocuped_Epath2 = True
        if D_Path1 and D_Path2 is None:
            for players in Player1:
                for players2 in Player2:
                    if players.position == Eat_Path1 or players2.position == Eat_Path1:
                        Ocuped_Epath1 = True
            if Ocuped_Epath1:
                return False
            else:
                return True
        if D_Path1 is None and D_Path2:
            for players in Player1:
                for players2 in Player2:
                    if players.position == Eat_Path2 or players2.position == Eat_Path2:
                        Ocuped_Epath2 = True
            if Ocuped_Epath2:
                return False
            else:
                return True
        if D_Path1 and D_Path2:
            for players in Player1:
                for players2 in Player2:
                    if players.position == Eat_Path2 or players2.position == Eat_Path2:
                        Ocuped_Epath2 = True
                    if players.position == Eat_Path1 or players2.position == Eat_Path1:
                        Ocuped_Epath1 = True
            if Ocuped_Epath2 and Ocuped_Epath1:
                return False
            elif Ocuped_Epath2 and Ocuped_Epath1 is None:
                return True
            elif Ocuped_Epath1 and Ocuped_Epath2 is None:
                return True

    @staticmethod
    # Esta funcion busca si la ficha puede dar el doble salto
    def Find_Path(S_Position, Turn_Player, Player1, Player2):
        if S_Position is None:
            return None
        A_Path1, A_Path2 = Ficha.Adayacend_moves(S_Position, Turn_Player)
        E_Path1, E_Path2 = Ficha.Adayacend_of_Adayacend(A_Path1, A_Path2, Turn_Player)
        Ocup_Path1, Ocup_Path2 = None, None
        if Turn_Player == 1:
            for players2 in Player2:
                if players2.position == A_Path1:
                    Ocup_Path1 = True
                if players2.position == A_Path2:
                    Ocup_Path2 = True
            if Ocup_Path1 is None and Ocup_Path2 is None:
                return None
            else:
                return Ficha.Find_Path2(Ocup_Path1, Ocup_Path2, E_Path1, E_Path2, Player1, Player2)
        else:
            for players in Player1:
                if players.position == A_Path1:
                    Ocup_Path1 = True
                if players.position == A_Path2:
                    Ocup_Path2 = True
            if Ocup_Path1 is None and Ocup_Path2 is None:
                return None
            else:
                return Ficha.Find_Path2(Ocup_Path1, Ocup_Path2, E_Path1, E_Path2, Player1, Player2)

    @staticmethod
    def Back_Path(vpos, Player1, Player2,  Turn_Player):
        Tpos = Ficha.True_position(vpos[0], vpos[1], Ficha.Moves_Squares())
        if Ficha.Checking_The_Queens(vpos, Player1, Player2, Turn_Player):
            if Turn_Player == 1:
                B_Path1, B_Path2 = (Tpos[0] - 75, Tpos[1] + 75), (Tpos[0] + 75, Tpos[1] + 75)
                return B_Path1, B_Path2
            else:
                B_Path1, B_Path2 = (Tpos[0] - 75, Tpos[1] - 75), (Tpos[0] + 75, Tpos[1] - 75)
                return B_Path1, B_Path2
        else:
            return None, None

    @staticmethod
    def Find_Path_to_Print(Position, Players1, Players2, Turn_Player):  # Aqui se imprime los caminos que puede recorrer la ficha
        First, Second, Third, Fourth = None, None, None, None
        if Ficha.Checking_The_Queens(Position, Players1, Players2, Turn_Player):
            Alternative1, Alternative2 = Ficha.Adayacend_moves(Position, Turn_Player)
            B_Path1, B_Path2 = Ficha.Back_Path(Position, Turn_Player)
            for player2 in Players2:
                for player in Players1:
                    if player.position == Alternative1 or player2.position == Alternative1:
                        First = True
                    elif player.position == Alternative2 or player2.position == Alternative2:
                        Second = True
                    elif player.position == B_Path1 or player2.position == B_Path1:
                        Third = True
                    elif player.position == B_Path2 or player2.position == B_Path2:
                        Fourth = True
            return First, Second, Third, Fourth
        else:
            Alternative1, Alternative2 = Ficha.Adayacend_moves(Position, Turn_Player)
            for player2 in Players2:
                for player in Players1:
                    if player.position == Alternative1 or player2.position == Alternative1:
                        First = True
                    elif player.position == Alternative2 or player2.position == Alternative2:
                        Second = True
            return First, Second, Third, Fourth

    @staticmethod
    def Adayacend_moves(pos, Turn_Player):  # Aqui se retorna las adyacentes de la ficha
        True_pos = Ficha.True_position(pos[0], pos[1], Ficha.Moves_Squares())
        if True_pos is None:
            return None, None
        if Turn_Player == 1:
            Path1 = (True_pos[0] - 75, True_pos[1] - 75)
            Path2 = (True_pos[0] + 75, True_pos[1] - 75)
            return Path1, Path2
        else:
            Path2 = (True_pos[0] + 75, True_pos[1] + 75)
            Path1 = (True_pos[0] - 75, True_pos[1] + 75)
            return Path1, Path2

    @staticmethod
    def Adayacend_of_Adayacend(pos1, pos2, Turn_Player):  # Aqui retorna las adyacentes de las adyacentes de la ficha
        if pos1 is None or pos2 is None:
            return None, None
        if Turn_Player == 1:
            Path_to_Eat1 = (pos1[0] - 75, pos1[1] - 75)
            Path_to_Eat2 = (pos2[0] + 75, pos2[1] - 75)
            if Path_to_Eat1[0] < 0:
                Path_to_Eat1 = 1
            elif Path_to_Eat2[0] > 600:
                Path_to_Eat2 = 1
            return Path_to_Eat1, Path_to_Eat2
        else:
            Path_to_Eat1 = (pos1[0] - 75, pos1[1] + 75)
            Path_to_Eat2 = (pos2[0] + 75, pos2[1] + 75)
            if Path_to_Eat1[0] < 0:
                Path_to_Eat1 = 1
            elif Path_to_Eat2[0] > 600:
                Path_to_Eat2 = 1
            return Path_to_Eat1, Path_to_Eat2

    @staticmethod
    def Moves_Squares():  # Recorre todos los cuadros que son validos para moverse
        AviableMoves = []
        Xposition = 0
        Yposition = 525
        for cicle in range(0, 34):
            AviableMoves.append((Xposition, Yposition))
            Xposition += 150
            if cicle == 4 or cicle == 13 or cicle == 21 or cicle == 29:
                Xposition = 75
                Yposition -= 75
            if cicle == 9 or cicle == 17 or cicle == 25:
                Xposition = 0
                Yposition -= 75
        return AviableMoves


    @staticmethod
    def Wrong_Squares():
        List_W_Moves = []
        Xposition = 0
        Yposition = 525
        for cicle in range(0, 34):
            List_W_Moves.append((Xposition, Yposition))
            Xposition += 150
            if cicle == 4 or cicle == 13 or cicle == 21 or cicle == 29:
                Xposition = 0
                Yposition -= 75
            if cicle == 9 or cicle == 17 or cicle == 25:
                Xposition = 75
                Yposition -= 75
        return List_W_Moves

    @staticmethod
    # Aqui se ejecuta el movimiento para comer de la ficha
    def Eating(zpos, zpos2, Turn_Player, Player1, Player2):
        Tposition = Ficha.True_position(zpos[0], zpos[1], Ficha.Moves_Squares())
        Tposition2 = Ficha.True_position(zpos2[0], zpos2[1], Ficha.Moves_Squares())
        if Turn_Player == 1:
            Path1, Path2 = Ficha.Adayacend_moves(zpos, Turn_Player)
            Eat_pos1, Eat_pos2 = Ficha.Adayacend_of_Adayacend(Path1, Path2, Turn_Player)
            if Ficha.Checking_The_Queens(Tposition, Player1, Player2, Turn_Player):
                B_Path1, B_Path2 = Ficha.Back_Path(Tposition, Player1, Player2, Turn_Player)
                for players2 in Player2:
                    if players2.position == Path1 or players2.position == Path2 or players2.position == B_Path1 or players2.position == B_Path2:
                        Eat_pos3, Eat_pos4 = (B_Path1[0] - 75, B_Path1[1] + 75), (B_Path2[0] + 75, B_Path2[1] + 75)
                        return Ficha.Eating_Piece(Tposition2, Path1, Path2, B_Path1, B_Path2, Eat_pos1, Eat_pos2, Eat_pos3, Eat_pos4)
            else:
                for players2 in Player2:
                    if Path1 == players2.position or Path2 == players2.position:
                        return Ficha.Eating_Piece(Tposition2, Path1, Path2, None, None, Eat_pos1, Eat_pos2, None, None)
        else:
            Path1, Path2 = Ficha.Adayacend_moves(zpos, Turn_Player)
            Eat_pos1, Eat_pos2 = Ficha.Adayacend_of_Adayacend(Path1, Path2, Turn_Player)
            if Ficha.Checking_The_Queens(Tposition, Player1, Player2, Turn_Player):
                B_Path1, B_Path2 = Ficha.Back_Path(zpos, Player1, Player2, Turn_Player)
                Eat_pos3, Eat_pos4 = (B_Path1[0] - 75, B_Path1[1] - 75), (B_Path2[0] + 75, B_Path2[1] - 75)
                return Ficha.Eating_Piece(Tposition2, Path1, Path2, B_Path1, B_Path2, Eat_pos1, Eat_pos2, Eat_pos3, Eat_pos4)
            else:
                return Ficha.Eating_Piece(Tposition2, Path1, Path2, None, None, Eat_pos1, Eat_pos2, None, None)

    @staticmethod
    # Esta funcion recorre la accion que si el jugador decide comer o no
    def Eating_Piece(click_pos, Path1, Path2, Path3, Path4, Eat_pos1, Eat_pos2, Eat_pos3, Eat_pos4):
        Took_Path1, Took_Path2, Took_Path3, Took_Path4, Took_E_Path1, Took_E_Path2, Took_E_Path3, Took_E_Path4 = None, None, None, None, None, None, None, None
        if Eat_pos1 == click_pos:
            Took_E_Path1 = 1
            return Took_E_Path1
        elif Eat_pos2 == click_pos:
            Took_E_Path2 = 2
            return Took_E_Path2
        elif Eat_pos3 == click_pos:
            Took_E_Path3 = 3
            return Took_E_Path3
        elif Eat_pos4 == click_pos:
            Took_E_Path4 = 4
            return Took_E_Path4
        elif Path1 == click_pos:
            Took_Path1 = 1.5
            return Took_Path1
        elif Path2 == click_pos:
            Took_Path2 = 2.5
            return Took_Path2
        elif Path3 == click_pos:
            Took_Path3 = 3.5
            return Took_Path3
        elif Path4 == click_pos:
            Took_Path4 = 4.5
            return Took_Path4


    def Transformando_Ficha_Reina(self, ubication="./Imagenes/Ficha_Naranja_Reina.png"):
        if self.color == "Naranja":
            self.image = pygame.image.load(ubication)
        else:
            self.image = pygame.image.load("./Imagenes/Ficha_Azul_Reina.png")
        self.Display.blit(self.image, self.position)
        self.queen_status = True

    def select_pieces(self, Xposition, Yposition, Display):
        if self.queen_status:
            if self.color == "Naranja":
                self.image = pygame.image.load("./Imagenes/Seleccion_Ficha_Naranja_Reina.png")
            else:
                self.image = pygame.image.load("./Imagenes/Seleccion_Ficha_Azul_Reina.png")
            Display.blit(self.image, (Xposition, Yposition))
            pygame.display.flip()
        else:
            if self.color == "Naranja":
                self.image = pygame.image.load("./Imagenes/Seleccion_Ficha_Naranja.png")
            else:
                self.image = pygame.image.load("./Imagenes/Seleccion_de_Ficha_Azul.png")
            Display.blit(self.image, (Xposition, Yposition))
            pygame.display.flip()



    def movement_pieces(self, Xposition, Yposition, Display):
        self.after_selection()
        self.position = (Xposition, Yposition)
        Display.blit(self.image, self.position)
        pygame.display.flip()

    def after_selection(self, ubication="./Imagenes/Ficha_Naranja.png"):
        if self.queen_status:
            if self.color == "Naranja":
                self.image = pygame.image.load("./Imagenes/Ficha_Naranja_Reina.png")
                pygame.display.flip()
            else:
                self.image = pygame.image.load("./Imagenes/Ficha_Azul_Reina.png")
                pygame.display.flip()
        else:
            if self.color == "Naranja":
                self.image = pygame.image.load(ubication)
                pygame.display.flip()
            else:
                self.image = pygame.image.load("./Imagenes/Ficha_Azul.png")
                pygame.display.flip()

    def eat_function(self):
        self.position = None


# class Op_Ficha(Ficha):
#     def __init__(self, Xposition, Yposition, Display):
#         self.imageop = pygame.image.load("./Imagenes/Ficha_Azul.png")
#         self.Display = Display
#         self.position = (Xposition, Yposition)
#         self.queen_status = False
#         self.Display.blit(self.imageop, self.position)
#
#     def select_pieces(self, Xposition, Yposition, Display):
#         if self.queen_status:
#             self.imageop = pygame.image.load("./Imagenes/Seleccion_Ficha_Azul_Reina.png")
#             Display.blit(self.imageop, (Xposition,Yposition))
#             pygame.display.flip()
#         else:
#             self.imageop = pygame.image.load("./Imagenes/Seleccion_de_Ficha_Azul.png")
#             Display.blit(self.imageop, (Xposition, Yposition))
#             pygame.display.flip()
#
#     def movement_pieces(self, Xposition, Yposition):
#         self.after_selection()
#         self.position = (Xposition, Yposition)
#         self.Display.blit(self.imageop, self.position)
#         pygame.display.flip()
#
#     def transform_ficha(self, ubication="./Imagenes/Ficha_Azul_Reina.png"):
#         self.imageop = pygame.image.load(ubication)
#         self.Display.blit(self.imageop, self.position)
#         self.queen_status = True
#
#     def after_selection(self, ubication="./Imagenes/Ficha_Azul.png"):
#         if self.queen_status:
#             self.imageop = pygame.image.load("./Imagenes/Ficha_Azul_Reina.png")
#             pygame.display.flip()
#         else:
#             self.imageop = pygame.image.load(ubication)
#             pygame.display.flip()
#
#     def eat_function(self):
#         self.position = None

# class Op_Ficha:
#     def __init__(self, Xposition, Yposition, Display):
#         self.imageop = pygame.image.load("Ficha_Azul.png")
#         self.Display = Display
#         self.position = (Xposition, Yposition)
#         self.queen_status = False
#         self.Display.blit(self.imageop, self.position)
#
#     def select_pieces(self, Xposition, Yposition, Display):
#         self.imageop = pygame.image.load("Seleccion_de_Ficha_Azul.png")
#         Display.blit(self.imageop, (Xposition, Yposition))
#         pygame.display.flip()
#
#     def movement_pieces(self, Xposition, Yposition):
#         self.after_selection()
#         self.position = (Xposition, Yposition)
#         self.Display.blit(self.imageop, self.position)
#         pygame.display.flip()
#
#     def transform_ficha(self, ubication="Ficha_Azul_Reina.png"):
#         self.imageop = pygame.image.load(ubication)
#         self.Display.blit(self.imageop, self.position)
#         self.queen_status = True
#
#     def after_selection(self, ubication="Ficha_Azul.png"):
#         self.imageop = pygame.image.load(ubication)
#         pygame.display.flip()
#
#     def eat_function(self):
#         self.position = None


class Tablero:
    def __init__(self, Display):
        self.board_image = pygame.image.load("./Imagenes/tablero_original.png")
        self.board = pygame.transform.scale(self.board_image, (600, 600))
        Display.blit(self.board, (0, 0))
