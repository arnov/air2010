from stemmer import PorterStemmer

def print_to_file(numericalArray, labels,train_data_loc, train_labels_loc):
    # Create files to save the output
    train_data = open(train_data_loc, 'w')    
    train_labels = open(train_labels_loc, 'w')
    
    # Print all the numerical data to the file
    for i in range(len(numericalArray)):  
        train_data.write(str(numericalArray[i]).strip('[]'))
        train_data.write('\n')
        train_labels.write(str(labels[i]).strip('[]'))
        train_labels.write('\n')

                
        #labelsMatlab.write(labels[lineno])
        #dataMatlab.write('\n')
        
def stem_word(sentence):
    for i in range(len(sentence)):
        p = PorterStemmer()
        sentence[i] = sentence[i].lower()
        sentence[i] = p.stem(sentence[i], 0,len(sentence[i])-1)        
    return sentence


def parse_url(sentence):
    wordsToAdd = []
    wordsToDelete = []
    for word in sentence:
        if word[0:4] == 'http':
            urlInfo = word.split('/')
            try:
                #print word
                #print urlInfo[2].strip('www.').split('.')[0]
                wordsToAdd.append(urlInfo[2].strip('www.').split('.')[0])
                wordsToDelete.append(word)
            except:
                continue
            
    # Use a list to delete and add words after the loop otherwise
    # the index of the previous loop will get messed up
    for word in wordsToDelete:
        sentence.remove(word)
    for word in wordsToAdd:
        sentence.append(word)
        
    return sentence
    
def remove_strange_symbols(sentence):
    # Remove strange symbols at the beggining and at the end of the terms
    for i in range(len(sentence)):
        sentence[i] = sentence[i].strip('.,:;&%()[]{}=+-*/\!|?~@#$\'')
    # Separate words that are seen as one term because istead of being separated by a space they are separated by a symbol
    symbols = ('.', '/', '-', '_', '\\')
    for symb in range(len(symbols)):
	    for i in range(len(sentence)):
		temp = sentence[i].split(symbols[symb])
		if (len(temp) > 1):
			sentence.remove(sentence[i])
		for j in range(len(temp)):
			if (temp[j] != ''):
				sentence.append(temp[j]) 
    return sentence
   
    
def remove_short_words(sentence,length):
    temp_list = []
    # Remove the words with a lengh lower that length
    for i in range(len(sentence)):
        if len(sentence[i]) < length:
            temp_list.append(sentence[i])
    
    for i in range (len(temp_list)):
        sentence.remove(temp_list[i])
    return sentence
    
def remove_stopwords(sentence):
    # Sorry :P
    stopWordList = ["a","about","above","across","after","again","against","all","almost","alone","along","already","also","although","always","among","an","and","another","any","anybody","anyone","anything","anywhere","are","area","areas","around","as","ask","asked","asking","asks","at","away","b","back","backed","backing","backs","be","became","because","become","becomes","been","before","began","behind","being","beings","best","better","between","big","both","but","by","c","came","can","cannot","case","cases","certain","certainly","clear","clearly","come","could","d","did","differ","different","differently","do","does","done","down","down","downed","downing","downs","during","e","each","early","either","end","ended","ending","ends","enough","even","evenly","ever","every","everybody","everyone","everything","everywhere","f","face","faces","fact","facts","far","felt","few","find","finds","first","for","four","from","full","fully","further","furthered","furthering","furthers","g","gave","general","generally","get","gets","give","given","gives","go","going","good","goods","got","great","greater","greatest","group","grouped","grouping","groups","h","had","has","have","having","he","her","here","herself","high","high","high","higher","highest","him","himself","his","how","however","i","if","important","in","interest","interested","interesting","interests","into","is","it","its","itself","j","just","k","keep","keeps","kind","knew","know","known","knows","l","large","largely","last","later","latest","least","less","let","lets","like","likely","long","longer","longest","m","made","make","making","man","many","may","me","member","members","men","might","more","most","mostly","mr","mrs","much","must","my","myself","n","necessary","need","needed","needing","needs","never","new","new","newer","newest","next","no","nobody","non","noone","not","nothing","now","nowhere","number","numbers","o","of","off","often","old","older","oldest","on","once","one","only","open","opened","opening","opens","or","order","ordered","ordering","orders","other","others","our","out","over","p","part","parted","parting","parts","per","perhaps","place","places","point","pointed","pointing","points","possible","present","presented","presenting","presents","problem","problems","put","puts","q","quite","r","rather","really","right","right","room","rooms","s","said","same","saw","say","says","second","seconds","see","seem","seemed","seeming","seems","sees","several","shall","she","should","show","showed","showing","shows","side","sides","since","small","smaller","smallest","so","some","somebody","someone","something","somewhere","state","states","still","still","such","sure","t","take","taken","than","that","the","their","them","then","there","therefore","these","they","thing","things","think","thinks","this","those","though","thought","thoughts","three","through","thus","to","today","together","too","took","toward","turn","turned","turning","turns","two","u","under","until","up","upon","us","use","used","uses","v","very","w","want","wanted","wanting","wants","was","way","ways","we","well","wells","went","were","what","when","where","whether","which","while","who","whole","whose","why","will","with","within","without","work","worked","working","works","would","x","y","year","years","yet","you","young","younger","youngest","your","yours","z","un","una","unas","unos","uno","sobre","todo","tambien","tras","otro","algun","alguno","alguna","algunos","algunas","ser","es","soy","eres","somos","sois","estoy","esta","estamos","estais","estan","como","en","para","atras","porque","por que","estado","estaba","ante","antes","siendo","ambos","pero","por","poder","puede","puedo","podemos","podeis","pueden","fui","fue","fuimos","fueron","hacer","hago","hace","hacemos","haceis","hacen","cada","fin","incluso","primero","desde","conseguir","consigo","consigue","consigues","conseguimos","consiguen","ir","voy","va","vamos","vais","van","vaya","gueno","ha","tener","tengo","tiene","tenemos","teneis","tienen","el","la","lo","las","los","su","aqui","mio","tuyo","ellos","ellas","nos","nosotros","vosotros","vosotras","si","dentro","solo","solamente","saber","sabes","sabe","sabemos","sabeis","saben","ultimo","largo","bastante","haces","muchos","aquellos","aquellas","sus","entonces","tiempo","verdad","verdadero","verdadera","cierto","ciertos","cierta","ciertas","intentar","intento","intenta","intentas","intentamos","intentais","intentan","dos","bajo","arriba","encima","usar","uso","usas","usa","usamos","usais","usan","emplear","empleo","empleas","emplean","ampleamos","empleais","valor","muy","era","eras","eramos","eran","modo","bien","cual","cuando","donde","mientras","quien","con","entre","sin","trabajo","trabajar","trabajas","trabaja","trabajamos","trabajais","trabajan","podria","podrias","podriamos","podrian","podriais","yo","aquel",""]
        
    # Delete all the occurences of stopWords in the sentence
    for i, stopWord in enumerate(stopWordList):
        if sentence.count(stopWord) > 0:                    
            for i in range(sentence.count(stopWord)):
                sentence.remove(stopWord)
    return sentence
    
def print_settings(stem, stopword,short,url,symbols):
    print "Using the following settings: \n"
    if(stem == "stem"):
        print "-Using the stemmed data"
    else:
        print "-Using the non-stemmed data"
    if(stopword == "remove_stopword"):
        print "-Stopwords are ignored"
    else:
        print "-Stopwords are not ignored"
    if(short == "remove_short"):
        print "-Short words ( < 3 chars ) are ignored"
    else:
        print "-Short words are not ignored"
    if(url == "stem_url"):
        print "-URLs are reduced to domain"
    else:
        print "-URLs are used as they are in the data"
    if(symbols == "remove_symbols"):
        print "-Symbols ( @$%@#!$ ) are removed"
    else:
        print "-Symbols are not removed"