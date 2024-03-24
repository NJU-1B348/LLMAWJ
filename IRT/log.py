def SRT_log(success:bool, msg:str, error:str= ""):
    if success:
        print("\033[32m[IRT]\033[0m " + msg)
    else:
        if error == "warning":
            print("\033[33m[IRT Warning]\033[0m " + msg)
        elif error == "fatal":
            print("\033[31m[IRT Fatal Error]\033[0m " + msg)
        else:
            print("\033[31m[IRT]\033[0m " + msg)