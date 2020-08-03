import os
import discord

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
