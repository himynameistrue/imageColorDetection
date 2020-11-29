""" 
------********************************************------
FINAL VERSION COLOR DETECTION
Requirements:
- all images in a folder
- all images in pgn format
- images without background
Result stored in a new csv file with the colums:
[filename, colorListHex, colorName]
------********************************************------
 """


import sys
import pandas as pd
import colorsys
from colorz import colorz
import os
from os.path import join
import csv


fields = ['color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv('colors_little.csv', skipinitialspace=True, usecols=fields, sep=';')


#function to get closest-matching color
def getColorName(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"])) 
        if d <= minimum :
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

            
def main():
    path = os.getcwd() #get folder / images path
    n = 5   #number of color detected
    
    import csv  #open csv result file
    with open('color_results.csv', mode='w') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        result_writer.writerow(["filename", "colorListHex", "colorName"])
                    
        for root, dirs, files in os.walk(path + "/"): # from your argv[1]
            for f in files:
                if((os.path.isdir(f) is False) and (f != ".DS_Store") and ("png" in f)):    #take only png images
                    filename = join(root, f)
                    colorName_str = ""
                    colors = colorz(filename, n=n)  
                    colorList = list(colors)    #get list of colors detected
                    for c in colorList:         #for each hex color get the name
                        c = c.lstrip('#')
                        c_rgb = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))     #convertion hex to rgb
                        c_name = getColorName(c_rgb[0], c_rgb[1], c_rgb[2])
                        colorName_str = colorName_str + "| " + c_name + "|"
                    #print(colorName_str)
                        
                    result_writer.writerow([filename, colorList, colorName_str])    #write the result in the result csv file
                            
        
# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 