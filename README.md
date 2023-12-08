# Spam-e-mail-detector
This is a Machine Learning project that aims to detect spam e-mails. Thus, it is a classification task based on language processing. It produces very satisfying results, reaching 97% of accuracy in test set. 
To achieve such metrics, many data ETL processes were applied, as it can be found in the preprocessing.py file. Then, the occurences of each word in each e-mail were counted, and the frequencies of the 100 most common words in each class (spam/not spam)
were employed as features of the classification. 
Model selection, hyperparameter adjustment and testing are present in training.py, while errror_analysis comprises a set of functions to analyze the classification performance through numeric reports and graphics.
