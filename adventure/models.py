from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    title = models.IntegerField(default=0)
    n_to = models.IntegerField(default=-1)
    s_to = models.IntegerField(default=-1)
    e_to = models.IntegerField(default=-1)
    w_to = models.IntegerField(default=-1)
    x = models.IntegerField(default=-1)
    y = models.IntegerField(default=-1)

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def __str__(self):
        output = f'\n'
        output += f'-- START ROOM PRINT --\n'
        output += f'Title: {self.title}\n'
        output += f'Desc: {self.description}\n'
        output += f'n_to: {self.n_to}\n'
        output += f's_to: {self.s_to}\n'
        output += f'e_to: {self.e_to}\n'
        output += f'w_to: {self.w_to}\n'
        output += f'-- END ROOM PRINT --\n'
        output += f'\n'


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        print('INITIALIZE CALL')
        print(self.currentRoom)
        self.currentRoom = Room.objects.first().id
        self.save()

    def room(self):
        print('INSIDE ROOM CALL')
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

    def __str__(self):
        output = f'\n'
        output += f'-- START PLAYER PRINT --\n'
        output += f'USER: {self.user}\n'
        output += f'CurrentRoom: {self.currentRoom}\n'
        output += f'UUID: {self.uuid}\n'
        output += f'-- END PLAYER PRINT --'
        output += f'\n'

        return output


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
