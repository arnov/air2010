# AUTHORS:      Modolo Davide & Veenstra Arno
# DATE:         28 May 2010

# DESCRIPTION: As the data set released was too small, we needed some extra negative example 
# (especially for the SVM) and for this reason we harvested new tweets from the web. This function 
# is used to control that these tweets are not containing any ambiguos company name and do not refer to them. 
# If they don't, we add them in the proper form in the train data and the label them as NEGATIVE (false).

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

