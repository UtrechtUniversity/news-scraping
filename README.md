
# geenstijl scraper

Project to scrape news articles from geenstijl archieve of May.
Sample URL: https://www.geenstijl.nl/archieven/maandelijks/2020/05/

## Researcher & engineers

Researchers:

- Tubergen, F.A. van (Frank)

Data Engineers:

- Vos, M.G. de (Martine)
- Shiva Nadi Najafabadi

## Installation

This project requires:
  - Python 3.7 or higher
  - MySQL 8.0.20 or higher
  -  Install the dependencies with the code below

  ```sh
  pip install -r requirements.txt
  ```

## Example usage 

``` sh
scrapy crawl geenstijl
```

## Links 

- https://www.geenstijl.nl/

## Specifications
Scraper is expected to return the following keys:




```python
%%html
<style> 
table td, table th, table tr {text-align:left !important;}
</style>
```


<style> 
table td, table th, table tr {text-align:left !important;}
</style>





| Key | Data type|Description |Example|
| --- | --- |--- | --- |
|article_id| string | The unique id of articles ||
|title|string |Title of the article|Schouten maakt klimaatcomplot van corona|
|article_info|string|A short paragraph between title and text|Meer sparerib distancing!|
|article_body|string| The full text of the document|
|created_at|datetime object |date and time of scraping|2020-06-07 03:24:15|
|image|string | List of the image urls|
|reactions|string |Number of reactions to each article|396 reacties|
|author|string |Author|@Van Rossem|
|publication_time|string | Time of publication|08:37	|
|publication_date|string |Date of publication, format: dd-mm-yy|01-05-20|
|doctype	|string | Source of the news| geenstijl.nl|
|url|string |URL to the article|https://www.geenstijl.nl/5153232/schouten-maak...|
|tags|string |List of tags|stikstof, klimaat, quatsch|
|twitter|string |Twitter link|https://www.twitter.com/intent/tweet?text=Scho...|
|facebook|string |Facebook link|https://www.facebook.com/sharer/sharer.php?u=h...|
|iframe|string |Iframe video links |


```python

```
