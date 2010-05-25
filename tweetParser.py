def main():
        

    data = open('..\Tweets\\frowny.txt.processed.2009.05.25', 'r')    
    brands = ["Best Buy", "Borders bookstore", "Renfe Cercanias", "CME group","Cuatro", "Delta Airlines", "Dunkin Donuts", "Ford Motor", "GAP", "El hormiguero", "Leap", "Lennar", "Real madrid", "Opera", "Overstock", "El Pais", "Palm", "El Pozo", "Research", "Southwest Arilines", "Sprint", "TAM", "Warner Bros"]
  
    noBrand = True
    lineno = 1
    for line in data:
        if lineno < 1000:

            lineList = line.split(';;')                 
            
            for brand in brands:
                if(lineList[5].rfind(brand) == -1):            
                    noBrand = True
                else:
                    noBrand = False
            if(noBrand == True):                
                print "none\t"+str(lineno)+"\t1\t"+lineList[5].strip("\n")+"\tFALSE"
            else:
                print "Bad sentence"
                print lineList[5]
                
            lineno += 1   


        
if __name__ == "__main__":    
    main()

