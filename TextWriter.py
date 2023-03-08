import os
import pathlib

def TextWriter(*objects, sep=' ', end='\n',flush=False):
    Toppath = str(pathlib.Path(__file__).parent.resolve())
    path = Toppath + str('\\Top_Assets\\')
    path = r'{}'.format(path)
    LogText = open(path + 'Log.txt', 'a+', encoding='UTF-8')

    # try:
    #     path = os.getcwd() + str('\\Top_Assets\\')
    #     path = r'{}'.format(path)
    #     LogText = open(path+'Log.txt', 'a+', encoding='UTF-8')
    # except:
    #     path = os.getcwd() + str('\\assets\\')
    #     path = r'{}'.format(path)
    #     LogText = open(path + 'Log.txt', 'a+', encoding='UTF-8')

    LogText.write(str(*objects) + str(end))
    LogText.close()

if __name__ == "__main__":
    Text = "Sample {}".format(123)
    TextWriter(Text)
    print(Text)