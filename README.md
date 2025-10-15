# saiht.de/blog

![GitHub License](https://img.shields.io/github/license/kreier/saiht-blog)
![GitHub Release](https://img.shields.io/github/v/release/kreier/saiht-blog)

Framework to generate saiht.de/blog structure in English and German.

## Structure

This affects the content of the folder `/blog/` of `https://saiht.de`. The content is found in the `html` directory of this repository.

### Guiding principles

- Each event is inside a folder by the structure `/YYYY/MM/DD` including all images, text files, PDF documents, `csv` data or else
- The text content is written in `README.md` and/or `LIESMICH.md` inside the same folder
- English is preferred and used by the `parse_md.py` program to create an `index.html` file in the same folder
- Additionally there is an article created in a folder `/en/YYYY-MM-DD_title_of_the_event_-_English_or_German_-_here/` with `index.html` and links to the images with `../../YYYY/MM/DD/image.jpg` relative links
- Each page has a link to the next and previous article. Articles in the `/YYYY/MM/DD` folders link to articles inside this folder, articles in the `/de/ ` or `/en/` folder link to respective articles in their respective folders.
- A share button links to the language-specific link
- A fourth article is created with an `index.html` at '/YYYY/MM/DD/title_of_the_event_in_lowercase/` folder
- Three overview sites are created: `/blog/index.html`, `/blog/de/index.html` and `/blog/en/index.html` with an overview of how many articles in total in the respective language are available. Below is a list of all the articles, sorted by date and separated by year in their respective language and folder
- Logfiles of the compilation are held in the `/log` folder as `log/YYYY-MM-DD_log.txt` with version, number of conversions, etc.


### Example

Let's say I visit the botanic garden in Nairobi on February 29th, 2000. All images for this post are located in `/2000/02/29` folder, for example the `garden.jpg` and the `banner.jpg`. The German article would be written in `LIESMICH.md` while the English would be in `README.md`. From this content, a file `index.html` is created, preferable in English. If not present, the German article will be used for the `index.html`.

The first line of the markdown files contains the title, so there is `# Visit to the Botanic Garden in Nairobi on February 29th, 2000 - no leap day!` in the `README.md` and `# Besuch im Botanischen Garten von Nairobi am 29. Februar 2000 - kein Schalttag!` in `LIESMICH.md`. There will be 4 `index.html` generated, and the locations are:

- 2000/02/29/
- 2000/02/29/visit_to_the_botanic_garden_in_nairobi_on_february_29th_2000_-_no_leap_day/
- en/2000-02-29_visit_to_the_botanic_garden_in_nairobi_on_february_29th_2000_-_no_leap_day/
- de/2000-02-29_besuch_im_botanischen_garten_von_nairobi_am_29_februar_2000_-_kein_schalttag/

The comma, dot and exclamation mark are removed for the folder names, and all uppercase letters are changed to lowercase. The spaces are replaced by an underscore character. This should at least work for German and English. Vietnamese and Russian are on my todo list.

## History

The website [saiht.de](https://saiht.de) exist since the end of 1999. And it is a special task to keep it updated. I tried some database founded approaches like wordpress, but exporting data and articles to a new platform was always a little hassle, and it does not work offline. In the end, I just want some static webpages that work online and offline in a structured manner. All kinds of ideas started since 2018, and finalized in October 2025 with a combination of python, html, css and javascript.
