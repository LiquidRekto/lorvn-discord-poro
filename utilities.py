import os

def getMergedStringChunks(array):
    merged = ""
    for chunk in array:
        merged += chunk
        if (array.index(chunk) < len(array) - 1):
            merged += " "
    return merged
