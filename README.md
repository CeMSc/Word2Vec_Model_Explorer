# Word2Vec_Model_Explorer
This is a simple Tkinter-based GUI application that helps you train and explore Word2Vec models using your own text files. Word2Vec is a popular technique in natural language processing (NLP) that uses **neural networks** to learn **word embeddings** or vector **representations of words**. These word embeddings can be used for various NLP tasks, such as term expansion, building taxonomies, semantic similarity search, and much more.

# Use Cases
The application allows you to **train new models**, **load existing models**, and **find related words and bigrams**.

- **Term Expansion**: With the trained model, you can find similar terms for a given word or phrase, which can be useful for expanding queries in search engines or creating a more comprehensive list of terms related to a specific topic.
- **Building Taxonomies**: By finding related words, you can create hierarchies of concepts and organize them into taxonomies or ontologies for knowledge management and information retrieval purposes.
- **Semantic Similarity Search**: The vector representations of words can be used to find semantically similar content in large text corpora, such as finding similar articles, documents, or sentences based on the context of the words.

![W2VME UI](/images/image.png?raw=true "W2VME UI")

# Running the Application
You can use the application in three different ways. You can either use the script without user interface via a **Jupiter file** located in "./Jupiter Notebook" or run the python script with a **user interface** via Word2Vec_Model_Explorer.py located in ./Application/. Alteratively, you can make a **portable executable file** of Word2Vec_Model_Explorer.py by using pyinstaller. I am not sharing a ready made exe file here because it would be too large for GitHub, but you can find a ready made exe file at this [link](https://www.dropbox.com/s/k628n46tvd31rk5/Word2Vec_Model_Explorer.exe?dl=0)

Here's a brief explanation of how to run the script using each of the three approaches:

### 1. Jupyter Notebook
To run the script without the user interface via the Jupyter notebook, follow these steps:
a. Navigate to the ./Jupyter Notebook folder in your local repository.
b. Open the app.ipynb file in Jupyter.
c. Run the cells one by one or use the "Run All" option in the Jupyter toolbar. The script will execute, and you can input your data and parameters directly in the notebook.

### 2. Python Script with User Interface
To run the Python script with the user interface, follow these steps:
a. Navigate to the ./Application folder in your local repository.
b. Locate the Word2Vec_Model_Explorer.py file.
c. Open a terminal or command prompt, and run the following command:
```
python Word2Vec_Model_Explorer.py
```
d. The user interface will appear, and you can interact with the application using the buttons and input fields.

### 3. Portable Executable File
To create a portable executable file of Word2Vec_Model_Explorer.py using PyInstaller, follow these steps:
a. Install PyInstaller using pip, if you haven't already:
```
pip install pyinstaller
```
b. Navigate to the ./Application folder in your local repository.
c. Run the following command in the terminal or command prompt to create a standalone executable:
```
pyinstaller --onefile Word2Vec_Model_Explorer.py
```
d. Once the executable is created, it will be located in the ./Application/dist folder. You can then distribute and run the portable Word2Vec_Model_Explorer.exe file on any compatible computer without requiring Python or the application's dependencies to be installed. I am not sharing the file here because it is too large for Github, but you can find a ready made exe file at this [link](https://www.dropbox.com/s/k628n46tvd31rk5/Word2Vec_Model_Explorer.exe?dl=0)

# License

This project is licensed under the GNU General Public License v3.0. Please read the LICENSE file for more information.

# How to cite

Scartozzi, Cesare M. (2023.) Word2Vec Model Explorer (Version 1.0). Available from https://github.com/CeMSc/Word2Vec_Model_Explorer.
