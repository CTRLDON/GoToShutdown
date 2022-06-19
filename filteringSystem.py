import datetime
# times to compare
times = ["04:00 pm" , "10:30 pm" , "01:00 am" , "01:45 pm" ,"11:44 pm" , "02:21 am" , "02:22 am" , "08:00 pm"]
n = datetime.datetime.now().strftime("%I:%M %p")

# The Main Function Of This Code
# That Compares And Filters Time!!!
def filterTime(timeList , wantedToCompare):
    
    # The Dict That Will Contain The Last Values
    returningDict = {}
    
    # For Loop To Enter Times In The Dict To Be Ready To Compare
    for time in timeList:
    
        hour = time[0:2]
        minu = time[3:5]
        
        # To Join Them Depending On Period
        if time.endswith("pm") or time.endswith("PM"):
    
            if int(hour) < 12:
    
                hour = int(hour) + 12
                returningDict[time] = int(str(hour)+minu)
    
            else:
    
                returningDict[time] = int(hour + minu)
    
        else:
    
            if int(hour) < 12:
    
                hour = int(hour) + 12
                returningDict[time] = int(str(hour)+minu)
    
            else:
    
                hour = int(hour) - 12
                returningDict[time] = int(str(hour) + minu)
    
    # Making The Wanted Time Ready For The Comparison
    hour = wantedToCompare[0:2]
    minu = wantedToCompare[3:5]
    
    # Doing The Same Thing As The Dict
    if wantedToCompare.endswith("PM"):
        
        if int(hour) < 12:
          
            hour = int(hour) + 12
            nowTime = int(str(hour)+minu)
        
        else:
            
            nowTime = int(hour + minu)

    elif wantedToCompare.endswith("AM"):
        
        if int(hour) < 12:
        
            hour = int(hour) + 12
            nowTime = int(str(hour)+minu)
       
        else:
       
            hour = int(hour) - 12
            nowTime = int(str(hour) + minu)
        
    theBiggestTimes = []
    theSmalledTimes = []
    
    for value in returningDict.values():
        
        if value > nowTime:
        
            theBiggestTimes.append(value)
        
        else:
    
            theSmalledTimes.append(value)
    
    if len(theBiggestTimes) > 0:
        
        smallestTime = min(theBiggestTimes)

    else:

        smallestTime = min(theSmalledTimes)
    
    for key,value in returningDict.items():
    
        if value == smallestTime:
    
            return key

if __name__ == '__main__':
    
    minTime = filterTime(times , n)
    print(minTime)