Description of obsproc-verification-tool

The attached script computes the differences and percent differences of files within a desginated directory.  
Also, there is a binv command from a linux command line and computes the differences for all the categories 
and produces a difference and percent difference.  Within the script, you can specify at the top of the script
the two different directories you want to compare.  Also, when on WCOSS2 make sure when you run the script to do a module 
load python/3.8.6 as it needs this module in order to run properly. If your running the code on Hera you need this module: module load intelpython/2023.2.0

Steps to run code on WCOSS2:

1.) module load python/3.8.6

2.) python script_20240716.py

Steps to run on Hera:

1.) module load intelpython/2023.2.0

2.) python script_20240716.py

*Note: for each case you should get back a message that either the dataset directories have matching or no matching data.  In the column named '_merged', if both datasets matched in both directories you will see 'both'; otherwise you'll get either 'right_only' or 'left_only'
