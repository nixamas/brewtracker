import datacapture, time

def runScript():
    print("Running Script...")
    datacapture.main()
    print("DONE!!!")
    
if __name__ == "__main__":
    while True:
        runScript()
        time.sleep(120) # 120 secs = 2 minutes