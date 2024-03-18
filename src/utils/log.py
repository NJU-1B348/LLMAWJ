"""_summary_ log module for LLMAWJ.
"""

def success(msg:str) -> None:
    print("\033[32m[LLMAWJ]\033[0m " + msg)
    
def warning(msg:str) -> None:
    print("\033[33m[LLMAWJ Warning]\033[0m " + msg)
    
def fatal(msg:str) -> None:
    print("\033[31m[LLMAWJ Fatal Error]\033[0m " + msg)