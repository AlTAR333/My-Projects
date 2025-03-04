# Class instanciation 

class board :

    def __init__(self,pieces: list):
        # Create the empty board
        self.current_board = [['XX' for x in range(8)] for y in range(8)]

        # Add the pieces 
        for piece in pieces :
            x, y = piece.get_position()
            self.current_board[x][y] = piece


    def print_board(self) -> None:
        """
        Print the current state of the board
        """
        printable_list = []
        for el in self.current_board :
            temp_list = []
            for el2 in el :
                if el2 != "XX" :
                    name = el2.get_name()
                    temp_list.append(name[0] + el2.get_color()[0] if name != "Knight" else "N" + el2.get_color()[0])
                else :
                    temp_list.append("XX")
            printable_list.append(temp_list)

        print("  0  1  2  3  4  5  6  7")
        for index,row in enumerate(printable_list) :
            current_line = str(index) + " "
            for square in row :
                current_line += square + " "
            print(current_line)



    def get_square(self,coordinates: tuple):
        """
        Return the piece located at the coordinates put in argument, 'XX' if nothing
        """
        return self.current_board[coordinates[0]][coordinates[1]]
    

    def change_square(self,coordinates: tuple,piece) -> None:
        """
        Change the piece at the coordinates put in arguments by the piece put in argument
        """
        self.current_board[coordinates[0]][coordinates[1]] = piece
        if piece != "XX" :
            piece.change_position(coordinates)
        


class piece :

    def __init__(self,position,name,color,id):
        self.position = position
        self.initial_position = position
        self.previous_position = position
        self.name = name
        self.color = color
        self.id = id
        self.move = 0


    def get_name(self) -> str:
        """
        Return the color of the piece
        """
        return self.name
    
    def get_position(self) -> tuple:
        """
        Return the position of the piece
        """
        return self.position
    

    def get_previous_position(self) -> tuple:
        """
        Return previous position of the piece
        """
        return self.previous_position


    def get_color(self) -> str:
        """
        Return the color of the piece
        """
        return self.color
    

    def get_id(self) -> int:
        """
        Return the id of the piece
        """
        return self.id
    
    def get_move(self) -> int:
        """
        Return the number of move played by the piece
        """
        return self.move

    def movement(self) -> None:
        """
        Defines piece movement vectors
        """
        if self.name == "Pawn" :
            
            # Variance of pawn direction (forward/backward) if black or white
            if self.color == "white" :
                index = -1
            else :
                index = 1

            # Check whether diagonal capture is possible (optimizable)
            vectors = [(index,0)] 
            if self.position[1]-1 in [i for i in range(8)]:
                upper_left_piece = current_board.get_square((self.position[0] + index, self.position[1]-1))
                left_piece = current_board.get_square((self.position[0], self.position[1]-1))
                if left_piece != "XX" :
                    left_piece_previous_vector = list(map(lambda x,y : x-y, left_piece.get_position(), left_piece.get_previous_position()))
                    if left_piece_previous_vector == [2,0] and left_piece.get_name() == "Pawn" :
                        vectors.append((index,-1))
                        current_board.change_square(left_piece.get_position(),"XX")
                if upper_left_piece != "XX" :
                    vectors.append((index,-1))

            if self.position[1]+1 in [i for i in range(8)]:
                upper_right_piece = current_board.get_square((self.position[0]+index, self.position[1]+1))
                right_piece = current_board.get_square((self.position[0], self.position[1]+1))
                if right_piece != "XX" :
                    right_piece_previous_vector = list(map(lambda x,y : x-y, right_piece.get_position(), right_piece.get_previous_position()))
                    if right_piece_previous_vector == [2,0] and right_piece.get_name() == "Pawn" :
                        vectors.append((index,1))
                        current_board.change_square(right_piece.get_position(),"XX")
                if upper_right_piece != "XX" :
                    vectors.append((index,1))

            if self.position == self.initial_position :
                vectors.append((index*2,0))


        if self.name == "Rook" :
            vectors = [(0,x-7) for x in range(15)] + [(x-7,0) for x in range(15)]

        if self.name == "Bishop" :
            vectors = [(x-7,x-7) for x in range(15)] + [(-(x-7),x-7) for x in range(15)]

        if self.name == "Queen" :
            vectors = [(x-7,x-7) for x in range(15)] + [(-(x-7),x-7) for x in range(15)] + [(0,x-7) for x in range(15)] + [(x-7,0) for x in range(15)]

        if self.name == "King" :
            vectors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]

        if self.name == "Knight" :
            vectors = [(-2,-1),(-2,1),(-1,-2),(1,-2),(2,-1),(2,1),(-1,2),(1,2)]

        self.vector = vectors


    def get_vector(self) -> list:
        """
        Return the piece vector's list 
        """
        return self.vector
    
    def add_move(self) -> None:
        """
        Add 1 to the number of move of the piece
        """
        self.move += 1

    def change_position(self,coordinates) -> None:
        """
        Change the piece position (coordinates)
        """
        self.previous_position = self.position
        self.position = coordinates


    def is_promoting(self) -> None:
        """
        Promote a pawn if he's on the last square of the board
        """
        if self.position[0] - self.initial_position[0] in [7,-7]:
            while True : 
                new_piece_name = input("Enter a valid piece name to promoto your pawn into (Queen, Knight, Bishop, Rook) : ")
                if new_piece_name in ["Queen", "Knight", "Bishop", "Rook"] :
                    self.name = new_piece_name
                    self.movement()
                    #id should change but i'm not using it yet so who cares


    def piece_in_the_way(self,current_vector: tuple) -> bool:
        """
        Return True if a piece is located between this piece and position indicated by the vector in argument
        """
        pos = list(current_vector)
        index_0_not_nul = False
        index_1_not_nul = False

        if current_vector[0] != 0 :
            index_0_not_nul = True
        if current_vector[1] != 0 :
            index_1_not_nul = True

        for _ in range(max(abs(current_vector[0]),abs(current_vector[1]))-1) :
            if index_0_not_nul :
                pos[0] = pos[0] - 1 if pos[0] > 0 else pos[0] + 1
            if index_1_not_nul :
                pos[1] = pos[1] - 1 if pos[1] > 0 else pos[1] + 1
            if current_board.get_square((self.position[0] + pos[0], self.position[1] + pos[1])) != "XX" :
                return True
            
        return False
    

    def is_check(self) -> bool:
        """
        Return True if the piece checks the opponent's king, else False
        """

        # If it's a pawn, we take back it's movement vectors (only keeping the ones where he eats something)
        if self.get_name() == "Pawn" :
            current_vectors = [x for x in self.vector if x not in [(1,0),(2,0),(-1,0),(-2,0)]]
        else :
            current_vectors = self.vector

        king_position_vector = (-1,-1)
        for vector in current_vectors :
            current_square_pos = (self.position[0] + vector[0], self.position[1] + vector[1])

            # We check if the piece "sees" a king
            if current_square_pos[0] in [i for i in range(8)] and current_square_pos[1] in [i for i in range(8)] :
                current_square = current_board.get_square(current_square_pos)
                if current_square != "XX" and current_square.get_name() == "King" and current_square.get_color() != self.color :
                    king_position_vector = vector

        # We check if a piece is in the way
        if king_position_vector != (-1,-1) :
            return not self.piece_in_the_way(king_position_vector)
        else :
            return False


    def is_checkmate(self) -> bool:
        """
        Return True if the king is checkmated, else False
        """

        # We check if the King can move on a safe square
        for vector in self.vector :
            current_square_pos = (self.position[0] + vector[0], self.position[1] + vector[1])
            if current_square_pos[0] in [x for x in range(8)] and current_square_pos[0] in [x for x in range(8)]:
                current_square = current_board.get_square(current_square_pos)
                if current_square == "XX" or current_square.get_color() != self.color :
                    current_board.change_square(current_square_pos,self)
                    current_board.change_square(self.position,"XX")
                    illegal_move = False
                    for el in check_pieces :
                        if el.is_check() :  
                            illegal_move = True
                    current_board.change_square(self.position,self)
                    current_board.change_square(current_square_pos,current_square)
                    if not illegal_move :
                        return False

        # We check if a piece can be played to block the checkmate or take the piece
        checkmate = True
        for el in check_pieces :
            if el.get_name() != "Knight" :

                # On récupère les cases où une pièce pourrait être jouée pour bloquer
                current_vector = [el.get_position()[0] - self.position[0], el.get_position()[1] - self.position[1]]
                if current_vector[0] != 0 :
                    index_0_not_nul = True
                if current_vector[1] != 0 :
                    index_1_not_nul = True

                list_square = []
                for _ in range(max(abs(current_vector[0]),abs(current_vector[1]))) :
                    list_square.append((self.position[0] + current_vector[0], self.position[1] + current_vector[1]))
                    if index_0_not_nul :
                        current_vector[0] = current_vector[0] - 1 if current_vector[0] > 0 else current_vector[0] + 1
                    if index_1_not_nul :
                        current_vector[1] = current_vector[1] - 1 if current_vector[1] > 0 else current_vector[1] + 1

                # On regarde si une pièce peut être jouée sur les cases 
                piece_list = white_pieces if self.color == "white" else black_pieces

                for el in piece_list :
                    piece_vector = el.get_vector()
                    piece_position = el.get_position()
                    for vector in piece_vector :
                        if (piece_position[0] + vector[0], piece_position[1] + vector[1]) in list_square :
                            if not el.piece_in_the_way(vector) :
                                # Vérif du clouage
                                current_board.change_square(piece_position,"XX")
                                for el2 in white_pieces if turn == "black" else black_pieces :
                                    if el2.is_check() and el2 not in check_pieces :
                                        current_board.change_square(piece_position,self)   
                                        pin = True
                                        break
                                    else :
                                        pin = False
                                if not pin :
                                    checkmate = False
                
        return checkmate


# Instance du board de base

pawn1b = piece((1,0),"Pawn","black",1)
pawn2b = piece((1,1),"Pawn","black",2)
pawn3b = piece((1,2),"Pawn","black",3)
pawn4b = piece((1,3),"Pawn","black",4)
pawn5b = piece((1,4),"Pawn","black",5)
pawn6b = piece((1,5),"Pawn","black",6)
pawn7b = piece((1,6),"Pawn","black",7)
pawn8b = piece((1,7),"Pawn","black",8)
rook1b = piece((0,0),"Rook","black",1)
rook2b = piece((0,7),"Rook","black",2)
bishop1b = piece((0,2),"Bishop","black",1)
bishop2b = piece((0,5),"Bishop","black",2)
knight1b = piece((0,1),"Knight","black",1)
knight2b = piece((0,6),"Knight","black",2)
queen1b =piece((0,3),"Queen","black",1)
king1b = piece((0,4),"King","black",1)

pawn1w = piece((6,0),"Pawn","white",1)
pawn2w = piece((6,1),"Pawn","white",2)
pawn3w = piece((6,2),"Pawn","white",3)
pawn4w = piece((6,3),"Pawn","white",4)
pawn5w = piece((6,4),"Pawn","white",5)
pawn6w = piece((6,5),"Pawn","white",6)
pawn7w = piece((6,6),"Pawn","white",7)
pawn8w = piece((6,7),"Pawn","white",8)
rook1w = piece((7,0),"Rook","white",1)
rook2w = piece((7,7),"Rook","white",2)
bishop1w = piece((7,2),"Bishop","white",1)
bishop2w = piece((7,5),"Bishop","white",2)
knight1w = piece((7,1),"Knight","white",1)
knight2w = piece((7,6),"Knight","white",2)
queen1w =piece((7,3),"Queen","white",1)
king1w = piece((7,4),"King","white",1)

white_pieces = [pawn1w, pawn2w, pawn3w, pawn4w, pawn5w, pawn6w, pawn7w, pawn8w, rook1w, rook2w, bishop1w, bishop2w, knight1w, knight2w, queen1w, king1w]
black_pieces = [pawn1b, pawn2b, pawn3b, pawn4b, pawn5b, pawn6b, pawn7b, pawn8b, rook1b, rook2b, bishop1b, bishop2b, knight1b, knight2b, queen1b, king1b]
list_pieces = [pawn1w, pawn2w, pawn3w, pawn4w, pawn5w, pawn6w, pawn7w, pawn8w, rook1w, rook2w, bishop1w, bishop2w, knight1w, knight2w, queen1w, king1w,
               pawn1b, pawn2b, pawn3b, pawn4b, pawn5b, pawn6b, pawn7b, pawn8b, rook1b, rook2b, bishop1b, bishop2b, knight1b, knight2b, queen1b, king1b]
current_board = board(list_pieces)

# Instance of movement vectors :
for el in list_pieces :
    el.movement()


# Instance graphique TO DO


# Game start
turn = 'white'
move = 0 
check = False
checkmate = False

while True :
    current_board.print_board()
    if checkmate :
        print("Checkmate !")
        exit()
    if check :
        print("Check !")
    print(f"{turn.title()} to play.")
    roque = False

    # We get the coordinates of the piece the player wants to move
    success = False
    while not success :
        initial_coordinates = input('Wich piece do you want to move ? y,x ')
        try :
            initial_coordinates = int(initial_coordinates[0]), int(initial_coordinates[2])
            if initial_coordinates[0] in [i for i in range(8)] and initial_coordinates[1] in [i for i in range(8)] :
                success = True
            else :
                raise IndexError
        except :
            print("Please enter valide coordinates in the valid format.")

    # We get the coordinates of the square the player wants to move
    success = False
    while not success :
        new_coordinates = input('Where do you want to move it ? y,x ')
        try :
            new_coordinates = int(new_coordinates[0]), int(new_coordinates[2])
            if initial_coordinates[0] in [i for i in range(8)] and initial_coordinates[1] in [i for i in range(8)] :
                success = True
            else :
                raise IndexError
        except :
            print("Please enter valide coordinates in the valid format.")

    current_vector = new_coordinates[0] - initial_coordinates[0], new_coordinates[1] - initial_coordinates[1]

    piece_ini_coords = current_board.get_square(initial_coordinates)
    piece_new_coords = current_board.get_square(new_coordinates)

    # Check castle
    
    if piece_ini_coords != "XX" and piece_ini_coords.get_name() == "King" and not check :
        if current_vector in [(0,2),(0,-2)] :
            supposed_rook = current_board.get_square((initial_coordinates[0],initial_coordinates[1] - 4 if current_vector == (0,-2) else initial_coordinates[1] + 3))
            conditions = (piece_ini_coords.get_move() == 0, supposed_rook != "XX", supposed_rook.get_name() == "Rook", supposed_rook.get_move() == 0, not piece_ini_coords.piece_in_the_way((0,3) if current_vector == (0,2) else (0,-4)))
            if all(conditions) :
                # We get the coordinates of the square seperating the 2 pieces
                if current_vector == (0,2) :
                    list_square = [(initial_coordinates[0],initial_coordinates[1]+1),(initial_coordinates[0],initial_coordinates[1]+2)]
                else :
                    list_square = [(initial_coordinates[0],initial_coordinates[1]-1),(initial_coordinates[0],initial_coordinates[1]-2),(initial_coordinates[0],initial_coordinates[1]-3)]

                # We transform them into Kings
                for square in list_square :
                    current_board.change_square(square,piece_ini_coords)

                # We check if an opponents piece check one of them
                check_square = False
                for el in white_pieces if turn == "black" else black_pieces :
                    if el.is_check() :
                        check_square = True

                # We switch the Kings back to empty squares
                for square in list_square :
                    current_board.change_square(square,"XX")

                # Castle
                if not check_square :
                    current_board.change_square(new_coordinates,piece_ini_coords)
                    current_board.change_square(initial_coordinates,"XX")
                    current_board.change_square(supposed_rook.get_position(),"XX")
                    current_board.change_square((new_coordinates[0],new_coordinates[1]+1) if current_vector ==(0,-2) else (new_coordinates[0],new_coordinates[1]-1),supposed_rook)
                    roque = True

    if not roque :
        # Illegal move check (empty inital square, opponents piece, capture of it's own piece, wrong move of a piece)

        if piece_ini_coords == "XX" :
            print("Illegal move.")
            continue
        else :
            piece_ini_coords_vector = piece_ini_coords.get_vector()
            piece_ini_coords_color = piece_ini_coords.get_color()

        if piece_new_coords == "XX" :
            piece_new_coords_color = None
        else : 
            piece_new_coords_color = piece_new_coords.get_color()

        if current_vector not in piece_ini_coords_vector or piece_ini_coords_color == piece_new_coords_color or piece_ini_coords_color != turn :
            print("Illegal move.")
            continue
        
        # Check if a piece is in the way
        if piece_ini_coords.get_name() != "Knight" :
            if piece_ini_coords.piece_in_the_way(current_vector) :
                print("Illegal move.")
                continue

        # Moving the piece
        current_board.change_square(new_coordinates,piece_ini_coords)
        current_board.change_square(initial_coordinates,"XX")

        # Check for pin or check 
        illegal_move = False 
        list_current_piece = white_pieces if turn == "black" else black_pieces

        for el in list_current_piece :
            if el.is_check() :
                print("Illegal move")
                current_board.change_square(new_coordinates,piece_new_coords)
                current_board.change_square(initial_coordinates,piece_ini_coords)
                illegal_move = True
                break
            elif el == list_current_piece[-1] :
                if piece_new_coords != "XX" :
                    black_pieces.remove(piece_new_coords) if turn == "white" else white_pieces.remove(piece_new_coords)
                            
                        
        if illegal_move :
            continue

        # 1 increment in the number of moves played by the piece (currently not very useful, only for castling)
        piece_ini_coords.add_move()

        # Checking a promotion
        if piece_ini_coords.get_name() == "Pawn" :
            piece_ini_coords.is_promoting()

        # Instance of pawn vectors
        for el in list_pieces :
            if el.get_name() == "Pawn" :
                el.movement()

    # Checking a check or chekmate
    check_pieces = []
    check = False

    for el in black_pieces if turn == "black" else white_pieces :
        if el.is_check() :
            check_pieces.append(el)
            if king1w.is_checkmate() if turn == "black" else king1b.is_checkmate() :
                checkmate = True
            else :
                check = True                 

    # Changing the player
    if turn == "white" :
        turn = "black"
    else :
        turn = "white"    

    move += 1



# A faire :
#   Interface graphique
#   Draw