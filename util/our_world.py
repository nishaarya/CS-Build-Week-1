from adventure.models import Room


class World:
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height

    def createBoard(self, new_width, new_height):
        self.width = new_width
        self.height = new_height

        # Create Empty Board
        board = [None] * new_height
        for row in range(len(board)):
            board[row] = [None] * new_width
        self.data = board

    def connectRooms(self, rooms):
        for room in rooms:
            # print(f'{room.x}, {room.y}')
            # print(f'{room.title}, {room.id}')

            # Connect to West
            if room.x - 1 >= 0:
                room.w_to = room.id - 1
            # Connect to East
            if room.x + 1 <= self.width:
                room.e_to = room.id + 1

            # Connect to South
            if room.y - 1 >= 0:
                room.s_to = room.id - self.height
            # Connect to North
            if room.y + 1 <= self.height:
                room.n_to = room.id + self.height

            room.save()

    def generateRoom(self, title, x, y):
        room = Room(title=title, x=x, y=y)
        room.save()

        # print(room)

    def populateWorld(self):
        roomCounter = 0
        x_counter = 0
        y_counter = 0

        for row_index in range(self.width):
            for column_index in range(self.height):
                # Make Room
                self.generateRoom(roomCounter, x_counter, y_counter)
                roomCounter += 1
                if x_counter >= self.width - 1:
                    x_counter = 0
                    y_counter += 1
                else:
                    x_counter += 1

        # Connect Rooms...
        allRooms = Room.objects.all()
        self.connectRooms(allRooms)
