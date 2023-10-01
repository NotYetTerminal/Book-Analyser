import pygal
import pandas as pd

dict_of_lists = {}

data = pd.read_csv("ending.csv")
for i, row in data.iterrows():
    dict_of_lists[row.Name] = [row.Length_of_book, row.Length_of_book_cleaned,
                               row.Average_length_of_words, row.Most_common_character,
                               row.Most_common_word]
    

chart = pygal.Bar()
chart.title = 'Length of book'
chart.x_labels = 'Original', 'Cleaned'
for key in dict_of_lists:
    chart.add(key, [dict_of_lists[key][0], dict_of_lists[key][1]])
    
chart.render_to_file('lengths.svg')
