
# GeenStijl scraper

Project aims to scrape news articles from geenstijl.nl and nu.nl.
Sample URLs: https://www.geenstijl.nl/, https://www.nu.nl/

## Researcher & engineers

Researcher:
- Frank van Tubergen

Project Manager:
- Laurence Frank

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
|id| string | The unique id of articles |a5154933|
|title|string |Title of the article|RIVM UPDATE: Deze week +4013 besmettingen|
|teaser|string|A short paragraph between title and text|Aantal nieuwe besmettingen STABILISEERT|
|text|string| The full text of the document|U mag kiezen:Optie 1:...|
|category|string| News section if any| null|
|created_at|datetime object |Date and time of scraping|2020-08-19 16:39:35|
|image|string | Dictionary of the image urls|{0: ''https://image.gscdn.nl/image/5f8b9b2526_Schermafbeelding... |
|reactions|string |Number of reactions to each article|308 reacties|
|author|string |Author|@Ronaldo|
|publication_time|string | Time of publication|14:20|
|publication_date|string |Date of publication, format: dd-mm-yy|18-08-20|
|doctype	|string | Source of the news| geenstijl.nl|
|url|string |URL to the article|https://www.geenstijl.nl/5154933/rivm-update-deze-week-4013-besmettingen/|
|tags|string |List of tags|corona, rivm|
|sitemap_url|string |Link to the site's sitemap if any|https://www.geenstijl.nl/sitemap.xml|



```python

```
