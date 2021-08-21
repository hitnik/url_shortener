# URL shortener APP

## URL shortener is cli application for generate,save and get from database short urls.

## Features

- Generating a short link from a long link.
- Save you cuctom long and short links, then het long link from short

## Installation

Clone git repository https://github.com/hitnik/url_shortener.git

```sh
git clone https://github.com/hitnik/url_shortener.git .
cd url_shortener
```

## Install Python dependencies

```console
python3 -m pip install -r requirements.txt
```

## Getting help

```console
python main.py -h
```

## Application use

To generate short url from long

```console
python main.py <long url> --generate
```

To save long and short urls

```console
python main.py <long url>  --generate --short_url <short url>
```

To get short url from long url

```console
python main.py <short url>
```
