FROM gitpod/workspace-full
RUN pyenv install 3.10.6 \
    && pyenv global 3.10.6
#RUN pip install pandas scikit-learn numpy seaborn nltk matplotlib pysastrawi textblob vader tqdm_notebook
RUN npm i learnpack -g
