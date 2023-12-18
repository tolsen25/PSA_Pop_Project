# PSA Pop Report Project

## Introduction 
The goal of this project is to scrape the pop report from the PSA website and explore use an EDA to explore the data.  To do so, I used python's BeautifulSoup package to scrape the pop report for each year that baseball cards were produced starting with 1861.  The resulting dataset is located at `data/allSets_wide.csv` which is over 26,250 rows.  The tidy data is in `data/longSets.csv` and is 314,989 rows.

### Images:
The plots created for the EDA are in the `images` folder.  Most of these images were created using plotnine, but some used Matplotlib.

## Pickle files
To save time loading in the data I saved files in .pkl files. These files are in the `pkl` folder

## Further Scraping
The `psa-card-scrape-master` folder is for the scraping individual sets of cards.  This tool is from the psa-scrape repository and can be viewed [here](https://github.com/ChrisMuir/psa-scrape).  This code was used to scrape data for a tableau story. 
