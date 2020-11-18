
# GeenStijl scraper

Project aims to scrape news articles from geenstijl.nl and nu.nl.
Sample URLs: https://www.geenstijl.nl/, https://www.nu.nl/

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
scrapy crawl nu

```

## Links 

- https://www.geenstijl.nl/
- https://www.nu.nl/

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
|Id| string | The unique identifier number of articles |a5156375|
|title|string |Title of the article|Stemcomputers stemmen in het Stamcafé|
|teaser|string|A short paragraph between title and text|Stemmen. Als een hele kleine viool|
|text|string| The body text of the news article|Weet je wat echt beroerd is voor het vertrouwen ...|
|category|string| News section if any| Null|
|publication_date_time|datetime object |Date and time of publication|2020-11-17 21:55:00|
|created_at|datetime object|Date and time of scraping|2020-11-17 23:00:06|
|images|string | Dictionary of the image urls if any|Null |
|reactions|string |Number of reactions to each article|202 reacties|
|author|string |Author|@Van Rossem|
|doctype	|string | Source of the news| geenstijl.nl|
|url|string |URL to the article|https://www.geenstijl.nl/5156375/stemcomputers-stemmen-in-het-stamcafe/|
|tags|string |List of tags|stamcafe, stemcomputers, stemmen|
|sitemap_url|string |Link to the website's sitemap if any|https://www.geenstijl.nl/sitemap.xml|



```python

```
