#!/usr/bin/env python
# coding: utf-8

# In[1]:


from RST_search import rst_search, tags_abbs, rels_abbs


# In[2]:


from flask import Flask
from flask import render_template, request, redirect
import json


# In[ ]:


app = Flask(__name__)

@app.route('/')
def start_page():
    return render_template('Test.html')

@app.route('/new')
def new_page():
    return render_template('New.html')

@app.route('/middle')
def middle_page():
    return render_template('Middle.html')

@app.route('/profi')
def profi_page():
    return render_template('Profi.html')

@app.route('/form')
def form():
    return render_template('search.html', pos_tags = tags_abbs, rels = rels_abbs)

@app.route('/results', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        input_query = request.form.get('input_query')
        selected_tags = request.form.getlist('pos_tag')        
        selected_rels = request.form.getlist('relation')
        
        input_query = None if input_query == '' else input_query
        selected_tags = None if selected_tags == [] else selected_tags
        selected_rels = None if selected_rels == [] else selected_rels

        results, text_ids = rst_search(input_query, selected_tags, selected_rels)
        if type(results) == list:
            list_len = len(results)
            return render_template('paral_res.html', result=results, list_len=list_len, text_ids=text_ids)
        else:
            return render_template('bad_entry.html', message = results)

if __name__ == '__main__':
    app.run("0.0.0.0")


# In[ ]:




