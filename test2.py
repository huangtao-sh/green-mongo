from glemon import config,P
config(is_dev=False)
from vacation import Holiday

obj= Holiday.find(P._id=='2020').first()

anpai=obj.anpai
anpai[1]='二、春节：1月24日至2月2日放假调休，共10天。1月19日（星期日）上班。'
obj.anpai=anpai
obj.save()

