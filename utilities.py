import os
import discord
from datetime import datetime, timezone, timedelta

def getUserDiscord(method, value):
    if (method == "by_name"):
        discord.utils.get()

def getMergedStringChunks(array):
    merged = ""
    for chunk in array:
        merged += chunk
        if (array.index(chunk) < len(array) - 1):
            merged += " "
    return merged

def getCurrentDatetime():
    return datetime.strftime((datetime.now(timezone.utc)),'%Y-%m-%d %H:%M:%S.%f')

#def returnSpecificTime(date, hour, minute, seconds):
 #   return datetime()

def dateTimeAddTime(timeObject, adays, ahours, aminutes, aseconds):
    if (ahours < 0 or aminutes < 0 or aseconds < 0 or adays < 0):
        return 'invalid'
    else:
        converted_time = datetime.strptime(timeObject, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.strftime((converted_time + timedelta(days = adays, hours = ahours, minutes = aminutes, seconds = aseconds)),'%Y-%m-%d %H:%M:%S.%f %Z')

def dateTimeSubtractTime(timeObject, sdays, shours, sminutes, sseconds):
    if (shours < 0 or sminutes < 0 or sseconds < 0 or sdays < 0):
        return 'invalid'
    else:
        converted_time = datetime.strptime(timeObject, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.strftime((converted_time + timedelta(days = sdays, hours = shours, minutes = sminutes, seconds = sseconds)),'%Y-%m-%d %H:%M:%S.%f %Z')

def dateTimeIsExpired(timeString):
    time_target = datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S.%f')
    time_now = datetime.strptime(getCurrentDatetime(), '%Y-%m-%d %H:%M:%S.%f')
    delta = time_target - time_now
    print (f"TIME_IN_DATABASE: {time_target}")
    print (f"TIME_TRIGGERED: {time_now}")
    print(delta.days)
    if (delta.days < 0):
        return True
    else:
        return False




