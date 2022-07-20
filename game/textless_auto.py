import textless
for i in range(100):
    print("loop:",i)
    if textless.looptrain() == 1:
        print('e')
# ------------------- alternative
#while textless.looptrain():
#    pass