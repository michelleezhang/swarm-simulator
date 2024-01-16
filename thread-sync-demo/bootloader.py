import importlib

class Bootloader():
    def __init__(self):
        print("INIT boot")
    
    # ######### UNEDITED #######################
    # def launch(self, id):
    #     fn = importlib.import_module("user.user")
    #     fn.usr(id)

    ######### OPTION ONE: Threading Barrier  #######################
    def launch(self, id, barrier):
        fn = importlib.import_module("user.user")
        fn.usr(id, barrier)