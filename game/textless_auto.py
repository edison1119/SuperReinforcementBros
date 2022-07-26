import textless
from importlib import reload
for i in range(100):
    print("loop:",i)
    reload(textless)
    if textless.looptrain() == 1:
        print('e')
# ------------------- alternative
#while textless.looptrain():
#    pass