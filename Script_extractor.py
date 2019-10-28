
import time
import os

            
def dynamic_search(path_models,path_file):
    
    debug = 1
    
    gen1 = [x for x in os.listdir("Files") if not x.startswith(".ipynb")]
    gen2 = [y for y in os.listdir("Models") if not y.startswith(".ipynb")]


    for i,file in enumerate(gen1) :
        if debug:
            print(file)
        file_extract = file
        for c,models in enumerate(sorted(gen2)) :
            create_matching_file(models,file_extract)
            #unique_match(models,file_extract)
            create_extract_file(models,file_extract)
            if debug:
                print("this is the file at the beginning of loop {0} : {1}\n".format(c,file_extract))

            file_extract = "ex_"+models.replace(".txt","_")+file_extract

            if debug:
                print("this is the extract file : {0}\n after modele : {1}\n".format(file_extract,models))

            
    


    if debug :
        print('Out of file loop {}'.format(i))
        




def move_files(path_file):
    #gen = (x for x in path_file if not x.startswith('.'))
    for file in path_file :
        if file.startswith("ex"):
            source = "Files/"+file
            destination = "Result/"+file
            os.rename(source,destination)


def write_matching_sentence(line_model,sentence,modele,file_to_filter):
    #sentence=sentence.lower().replace("-","")
    debug = 0
    mots_clés = [x for x in line_model.strip("\n").split(" ")]
    mots_phrase = [y for y in sentence.strip("\n").split(" ")]
    if debug:
        print("those are our words in model and in file_to_filter split and turned into a list :\n model : {0}\n file : {1}".format(mots_clés,mots_phrase))
    if set(mots_clés).issubset(mots_phrase) == True: 
        
        with open('Match/matching_'+modele.replace(".txt","_")+file_to_filter,"a") as f:
            f.write("{}\n".format(sentence.lower().strip("\n")))
        return "Found Match"    


def create_matching_file(modele,file_to_filter):
    #Create a file where we'll append the matching sentences after each model
    debug = 0 
    open('Match/matching_'+modele.replace(".txt","_")+file_to_filter, 'w').close()
    
    with open("Files/"+file_to_filter,"r") as file2: #file that you want to filter
        for sentence in file2:
            already_written = False
            with open("Models/"+modele,"r") as model:       
                for line_model in model:
                    if already_written == False:
                        if write_matching_sentence(line_model,sentence,modele,file_to_filter) == "Found Match":
                            if debug:
                                print(line_model)
                                print("This is the sentence that matches the model : {}\n".format(sentence))
                            already_written = True

    file2.close()




def create_extract_file(modele,file):  
    debug = 0    
    #create a file that will store the original file_to_filter without sentences of matching_file       
    open("Files/ex_"+modele.replace(".txt","_")+file, 'w').close()
    with open("Files/"+file,"r") as file2: #file that you want to filter
        for sentence in file2:
            with open('Match/matching_'+modele.replace(".txt","_")+file,'r') as matching_sentences:
                for line in matching_sentences:
                    if debug:
                        print("this line completes the model requirements : {} \n".format(line))
                    if line.strip("\n").lower() == sentence.strip("\n").lower():
                        sentence = sentence.replace(sentence,"")
                        
                with open("Files/ex_"+modele.replace(".txt","_")+file,'a') as new_content :
                     new_content.write(sentence.lower())
                     

def main():
    
   # parser = create_argument_parser()
    #cmdline_args = parser.parse_args()
    start= time.time()
    
    dynamic_search(os.listdir("Models"),os.listdir("Files"))
    move_files(os.listdir("Files")) 
    print("The script took: {} ".format(time.time()-start))
if __name__ == '__main__':  # pragma: no cover
    main()