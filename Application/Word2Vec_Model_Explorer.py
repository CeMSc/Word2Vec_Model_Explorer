import os
import re
import time
import pickle
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser


def read_data_from_folder(folder_path):
    texts = []
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                texts.append(f.read())
    return texts


def preprocess_text(text):
    return re.sub(r'\W+', ' ', text.lower()).split()


def train_word2vec_model(sentences):
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    model.train(sentences, total_examples=len(sentences), epochs=10)
    return model


def find_related_words_and_bigrams(model, phraser, words_and_bigrams, top_n=30):
    related_words_dict = {}
    for word_or_bigram in words_and_bigrams:
        if ' ' in word_or_bigram:
            splitted = word_or_bigram.split(' ')
            if phraser[splitted] == splitted:
                print(f"Bigram '{word_or_bigram}' not found in the model.")
                continue
            else:
                word_or_bigram = '_'.join(splitted)
        try:
            related_words = model.wv.most_similar(word_or_bigram, topn=top_n)
            related_words_dict[word_or_bigram.replace('_', ' ')] = related_words
        except KeyError:
            print(f"Word or bigram '{word_or_bigram.replace('_', ' ')}' not found in the model.")
    return related_words_dict


def train_model_from_folder(folder_path):
    texts = read_data_from_folder(folder_path)
    sentences = [preprocess_text(text) for text in texts]

    phrases = Phrases(sentences, min_count=1, threshold=10)
    phraser = Phraser(phrases)
    bigram_sentences = [phraser[sentence] for sentence in sentences]

    model = train_word2vec_model(bigram_sentences)
    return model, phraser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Word2Vec Model Explorer')
        self.geometry('600x700')

        # create widgets
        
        self.label = tk.Label(self, text='Welcome to Word2Vec Model Explorer!')
        self.label.pack(pady=10)
        
        self.license_button = tk.Button(self, text='License Agreement', command=self.show_license_agreement)
        self.license_button.pack(pady=3)
        
        self.license_button = tk.Button(self, text='How It Works', command=self.show_how_it_works)
        self.license_button.pack(pady=3)
        
        self.text1_label = tk.Label(self, text="Train a Word2Vec model on txt files.\n Training time may vary based on data size and computational power.\n The model will be saved in a folder call 'models'.") 
        self.text1_label.pack(pady=5)
        
        self.train_model_button = tk.Button(self, text='Train New Model', command=self.train_model)
        self.train_model_button.pack(pady=10)
        
        self.text2_label = tk.Label(self, text="Use an existing Word2Vec model by\n loading the .model and .pkl files.") 
        self.text2_label.pack(pady=5)

        self.load_model_button = tk.Button(self, text='Load Existing Model', command=self.load_model)
        self.load_model_button.pack(pady=10)

        self.model_loaded = False

        self.input_words_label = tk.Label(self, text='Enter words and bigrams separated by commas:')
        self.input_words_label.pack(pady=10)

        self.input_words_entry = tk.Entry(self)
        self.input_words_entry.pack(pady=10)

        self.run_button = tk.Button(self, text='Run', command=self.run)
        self.run_button.pack(pady=10)
        
        self.text3_label = tk.Label(self, text="The results are printed in the window below and saved in a file called output.tsv.") 
        self.text3_label.pack(pady=5)
        
        self.elapsed_time_text = tk.Label(self, text='Elapsed time: 0s')
        self.elapsed_time_text.pack(pady=10)

        self.output_text = tk.Text(self)
        self.output_text.pack(pady=10)
        
    def train_model(self):
        self.folder_path = filedialog.askdirectory(title='Choose a folder with text files')
        if not self.folder_path:
            return
        
        start_time = time.time()
        self.model, self.phraser = train_model_from_folder(self.folder_path)
        end_time = time.time()
        self.elapsed_time_text.config(text=f'Elapsed time: {end_time - start_time:.4f}s')

        self.model_loaded = True
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, 'The Word2Vec model was trained and saved successfully. You can now enter enter the terms and click "Run"')
        self.save_model(self.model, self.phraser)

    def load_model(self):
        model_path = tk.filedialog.askopenfilename(title='Choose a .model file', filetypes=[('Word2Vec Model', '*.model')])
        if not model_path:
            return

        phraser_path = tk.filedialog.askopenfilename(title='Choose a .pkl file', filetypes=[('Phraser', '*.pkl')])
        if not phraser_path:
            return

        with open(phraser_path, 'rb') as f:
            self.phraser = pickle.load(f)

        self.model = Word2Vec.load(model_path)
        self.model_loaded = True

        # Update output_text widget
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, 'The Word2Vec model loaded successfully. You can now enter enter the terms and click "Run"')


    def run(self):
        if not self.model_loaded:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, 'Please load or train a model first. You can train a model by clicking "Train New Mode" and select a folder containing one or more txt files. You can load a model that was previously created with this app by clicking on “Load Existing Model” and then select one .model and one .pkl files.')
            return

        input_words = self.input_words_entry.get().lower().strip().split(',')
        input_words = [word.strip() for word in input_words]

        self.output_text.delete('1.0', tk.END)
        self.elapsed_time_text.pack(pady=10)

        start_time = time.time()
        related_words_dict = find_related_words_and_bigrams(self.model, self.phraser, input_words)
        end_time = time.time()

        self.elapsed_time_text.config(text=f'Elapsed time: {end_time - start_time:.4f}s')
        
        self.save_to_csv(related_words_dict, file_name='output.tsv')
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(str(related_words_dict))

        output_str = '\n'.join([f'{key}: {value}' for key, value in related_words_dict.items()])
        self.output_text.insert(tk.END, output_str)
        
    def save_to_csv(self, related_words_dict, file_name='output.tsv'):
        df = pd.DataFrame(related_words_dict)
        for col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x[0].replace('_', ' ')}: {x[1]:.4f}")
        df.to_csv(file_name, index=False,sep='\t', encoding='utf-8')
    
    def save_model(self, model, phraser, folder_path='./models'):
        os.makedirs(folder_path, exist_ok=True)
        model.save(os.path.join(folder_path, 'word2vec.model'))
        with open(os.path.join(folder_path, 'phraser.pkl'), 'wb') as f:
            pickle.dump(phraser, f)
            
    def show_license_agreement(self):
        license_window = tk.Toplevel(self)
        license_window.title("License Agreement")
        license_window.geometry("600x800")
        
        license_text = '''
        Word2vec Model Explorer (W2VME)
        Cesare M. Scartozzi, Ph.D.
        Contact information available at: www.scartozzi.eu

        TERMS GOVERNING THE USE OF THE SOFTWARE
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License v3.0.

        This program is distributed in the hope that it will be useful,
        but without any warranty; without even the implied warranty of
        merchantability or fitness for a particular purpose. See the
        GNU General Public License for more details.

        You should download a copy of the GNU General Public License from https://www.gnu.org/licenses/. By installing the Software, you agree to be bound by the terms of the license. 
        '''
        license_label = tk.Label(license_window, text=license_text, wraplength=600)
        license_label.pack(padx=20, pady=20)

        close_button = tk.Button(license_window, text="Close", command=license_window.destroy)
        close_button.pack(pady=10)
    
    def show_how_it_works(self):
        license_window = tk.Toplevel(self)
        license_window.title("About Word2Vec Model Explorer")
        license_window.geometry("600x800")
        
        license_text = '''
        How to Use:
        Train New Model: Click this button to select a folder containing text files (.txt) you want to use for training a new Word2Vec model. The application will train the model and save it in the 'models' folder along with the Phraser used for bigrams.
        Load Existing Model: If you already have a trained model, click this button to load the .model and .pkl (Phraser) files. Make sure you select both files for the application to work properly.
        Enter words and bigrams: After loading or training a model, enter the words and bigrams you want to find related terms for in the input field, separated by commas.
        Run: Click this button to run the analysis. The application will display the results in the text area below and also save them in a TSV file named output.tsv. 
        
        Key Word 2 Vec parameters: vector_size=100, window=5, min_count=1, workers=4
        Find the full code at: https://github.com/CeMSc/Word2Vec_Model_Explorer
        
        '''
        license_label = tk.Label(license_window, text=license_text, wraplength=600)
        license_label.pack(padx=20, pady=20)

        close_button = tk.Button(license_window, text="Close", command=license_window.destroy)
        close_button.pack(pady=10)
        
if __name__ == '__main__':
    app = App()
    app.mainloop()
