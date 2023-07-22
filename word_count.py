import concurrent.futures
import spacy
import pandas as pd
from sqlalchemy import create_engine
from textacy import extract
from glob import glob

engine = create_engine("sqlite:///database.sqlite")
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 10000000 #Increase the max length of the text to process

#Create a function to return the list of files to process
def return_forms(datadir = "./data/*/*/*"):
#Create a List of Downloaded files  
    print('Creating the list of files')
    #datadir = "./data/*/*/*"
    forms = glob(datadir, recursive=True)

    #keep only the 10-k forms
    print('filtering only the 10-K forms')
    forms = {file for file in forms if file.split('_')[1][:4] == '10-K'}

    #Remove the processed files
    print('Removing the processed files')
    processed_files = pd.read_sql('SELECT accession_number FROM form_data', con=engine)
    processed_files = set(processed_files['accession_number'].tolist())
    forms = [file.replace('\\','/') for file in forms if file.split('_')[5].split('.')[0] not in processed_files]
    return forms


#Creates the function to Clean the text, remove punctuation, stopwords, and lemmatize the text
def process_text(text):
    sentences = list(nlp(text, disable=['ner', 'entity_linker', 'textcat', 'entitry_ruler']).sents)
    lemmatized_sentences = []
    for sentence in sentences:
        lemmatized_sentences.append([token.lemma_ for token in sentence if not token.is_stop and token.is_alpha])
    return [' '.join(sentence) for sentence in lemmatized_sentences]

#Create a function to load the dictionaries
def load_dictionary(path):
    with open(path) as f:
        dictionary = f.readlines()
    dictionary = {word.strip() for word in dictionary}
    return dictionary

#Create a function to count the words in the text
def count_words(text, dictionary):
    counter = 0
    for sentence in text:
        for word in sentence.split():
            if word.lower() in dictionary:
                counter += 1
    return counter

#Create a function to count the ngrams in the text
def count_ngram(ngrams, dictionary):
    counter = 0
    for ngram in ngrams:
        if ngram.lower() in dictionary:
            counter += 1
    return counter

#Create a function to create the ngrams
def create_ngram(text, n, sep='_'):
    doc = nlp(text,disable=['ner', 'entity_linker', 'textcat', 'entitry_ruler'])
    ngrams = extract.ngrams(doc, n, filter_stops=True, filter_punct=True, filter_nums=True, min_freq=1)
    ngrams = [ngram.lemma_ for ngram in ngrams]
    ngrams = [sep.join(ngram.lower().split()) for ngram in ngrams]
    return ngrams

#Create a function to process the files
def get_form_data(file,doc_number,total_queue):

    print('Processing items from file {}/{} - {}'.format(doc_number+1,total_queue, file))

    #create a dictionary with the form data
    form_data = dict()
    form_data['year'] = file.split('/')[2]
    form_data['filling_date'] = file.split('/')[-1].split('_')[0]
    form_data['form_type'] = file.split('_')[1]
    form_data['cik'] = file.split('_')[4]
    form_data['accession_number'] = file.split('_')[5].split('.')[0]

    #Open the file
    with open(file) as f:
        corpus = f.read()
    clean_text = process_text(corpus)

    #Create the basic features
    form_data['sentences'] = len(clean_text)
    form_data['words'] = sum([len(sentence.split()) for sentence in clean_text])
    
    #Create the unigrams
    form_data['innovation'] = count_words(clean_text, innovation_dictionary)
    form_data['integrity'] = count_words(clean_text, integrity_dictionary)
    form_data['quality'] = count_words(clean_text, quality_dictionary)
    form_data['respect'] = count_words(clean_text, respect_dictionary)
    form_data['teamwork'] = count_words(clean_text, teamwork_dictionary)

    #Create the bigrams
    bi_grams = create_ngram(' '.join(clean_text), 2,sep = '_')
    form_data['bi_innovation']  = count_ngram(bi_grams, innovation_dictionary)
    form_data['bi_integrity']  = count_ngram(bi_grams, integrity_dictionary)
    form_data['bi_quality']  = count_ngram(bi_grams, quality_dictionary)
    form_data['bi_respect']  = count_ngram(bi_grams, respect_dictionary)
    form_data['bi_teamwork']  = count_ngram(bi_grams, teamwork_dictionary)
    
    #Create the trigrams
    tri_grams = create_ngram(' '.join(clean_text), 3,sep = '_')
    form_data['tri_innovation']  = count_ngram(tri_grams, innovation_dictionary)
    form_data['tri_integrity']  = count_ngram(tri_grams, integrity_dictionary)
    form_data['tri_quality']  = count_ngram(tri_grams, quality_dictionary)
    form_data['tri_respect']  = count_ngram(tri_grams, respect_dictionary)
    form_data['tri_teamwork']  = count_ngram(tri_grams, teamwork_dictionary)

    #Save the data to the database
    df = pd.DataFrame(form_data, index=[0])
    df.to_sql('form_data', con=engine, if_exists='append', index=False)

    return

#Create a function to multi process the files
def get_form_multi(files_to_extract,max_workers = 8):
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        total_queue  = len(files_to_extract)
        for file ,doc_number in zip(files_to_extract, range(0,total_queue)):
            executor.submit(get_form_data, file,doc_number,total_queue)


#Load the dictionary
innovation_dictionary = load_dictionary('./dictionaries/Innovation.txt')
integrity_dictionary = load_dictionary('./dictionaries/Integrity.txt')
quality_dictionary = load_dictionary('./dictionaries/Quality.txt')
respect_dictionary = load_dictionary('./dictionaries/Respect.txt')
teamwork_dictionary = load_dictionary('./dictionaries/Teamwork.txt')


if __name__ == "__main__":

    #Create a List of Downloaded files
    forms = return_forms()

    #Process the files
    get_form_multi(forms,max_workers = 8)
