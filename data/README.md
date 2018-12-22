## Amazon Review Data from Julian McAuley, UCSD

We analyzed the product reviews and meta data of the Cell Phones and Accessories category of Amazon Review Data available on http://jmcauley.ucsd.edu/data/amazon/links.html. The data files were too huge to be uploaded on GitHub. 

We used a Linux machine on Google Cloud Platform. The data was saved into the virtual machine using:
#### 1. Review Data - 

wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Cell_Phones_and_Accessories.json.gz

gunzip --keep reviews_Cell_Phones_and_Accessories.json.gz

#### 2. Meta Data - 

wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Cell_Phones_and_Accessories.json.gz

gunzip --keep reviews_Cell_Phones_and_Accessories.json.gz


This unzipped the JSON files of the data sets, which were then read into Python for further analysis.
