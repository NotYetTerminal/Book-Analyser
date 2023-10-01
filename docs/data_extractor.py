import re
import pandas as pd
import glob
import csv

used= ['[\u0041-\u005A]', '[\u0061-\u007A]', '[\u00C0-\u01FF]', '[\u0400-\u04FF]',
       '[\u3300-\uA07F]', '[\u0020]']

# joins a list into a string
def jointhem(turp):
    over = ' '
    return (over.join(turp))

# gets a list an an input and returns a list with the most common whatever
# in that list
def mostcommon(listing):
    temp_dict = {}
    
    for chara in listing:
        if chara in temp_dict:
            temp_dict[chara]-=-1
        else:
            temp_dict[chara] = 1
            
    common_whatever = []
    try:
        del temp_dict[' ']
    except:
        pass
    search_value = max(temp_dict.values())
    
    for name, value in temp_dict.items():
        if value == search_value:
            common_whatever.append(name)
    
    return common_whatever
    
name_of_file = []
#puts txts into a list
for files in glob.glob('text\\*.txt'):
    name_of_file.append(files)
        
        
output = pd.DataFrame(columns=['Name', 'Length_of_book', 'Length_of_book_cleaned',
                                   'Average_length_of_words', 'Most_common_character',
                                   'Most_common_word'])

output = output.append({'Name': 'Name',
                        'Length_of_book': 'Length_of_book',
                        'Length_of_book_cleaned': 'Length_of_book_cleaned',
                        'Average_length_of_words': 'Average_length_of_words',
                        'Most_common_character': 'Most_common_character',
                        'Most_common_word': 'Most_common_word',
                        }, ignore_index = True)


#opens file and splits it into words
for file in name_of_file:
    split_by_function = []
    temp = []
    endlist = []
    with open(file, encoding="utf-8-sig") as book:
    
        textdata = book.read()
        textdata = textdata.lower()
    
        split_by_function = textdata.splitlines(keepends=True)
    
        #splits words into letters
        for item in split_by_function:
            word_split = list(item)
        
            #checks for non-letter characters
            for x in word_split:
                for i in used:
                    if bool(re.search(i, x)):
                        temp.append(x)
            
            #joins them back up in a list
            endlist.append(''.join(temp))
            temp.clear()
            word_split.clear()
        #https://www.utf8-chartable.de/unicode-utf8-table.pl?start=128&number=128&names=-&utf8=string-literal

    #takes out null
    for stuff in endlist:
        if stuff == '':
            endlist.remove(stuff)
        else:
            stuff.replace(' ', '')
            
            
    #joins the list back into a string
    final = jointhem(endlist)
    
    # gets most common letter(s)
    common_char = mostcommon(final)

    # average word length
    finalsplit = final.split()
    common_word = mostcommon(finalsplit)
    average_word = sum(len(word) for word in finalsplit) / len(finalsplit)

    # write to panda file
    file = file.split('\\')
    file = file[1]
    file = file[:-4]
    if file != 'chinese':
        output = output.append({'Name': file,
                                'Length_of_book': len(textdata),
                                'Length_of_book_cleaned': len(final),
                                'Average_length_of_words': average_word,
                                'Most_common_character': common_char[0],
                                'Most_common_word': common_word[0],
                                }, ignore_index = True)
    
    else:
        output = output.append({'Name': file,
                                'Length_of_book': len(textdata),
                                'Length_of_book_cleaned': len(final),
                                'Average_length_of_words': None,
                                'Most_common_character': common_char[0],
                                'Most_common_word': None
                                 }, ignore_index = True)
    

# write to csv file
with open('ending.csv', encoding="utf-8-sig", mode='w+', newline='') as f:
    writer = csv.writer(f)
    for i, row in output.iterrows():
        writer.writerow(row)

print('DONE')