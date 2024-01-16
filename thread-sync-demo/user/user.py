# ######### UNEDITED #######################
# def usr(id):
#     print(f"STEP 1 user {id}")
#     print(f"STEP 2 user {id}")
#     print(f"STEP 3 user {id}")
    
######### OPTION ONE: Threading Barrier  #######################
def usr(id, barrier):
    print(f"STEP 1 user {id}")
    barrier.wait()
    print(f"STEP 2 user {id}")
    barrier.wait()
    print(f"STEP 3 user {id}")
    barrier.wait()
