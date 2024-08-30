# Web font generator

Web font generator splits the Japanese web font specified by Google Fonts into about 120 subsets and converts them to .woff2 format.

# Configuration

## Set your Google API key

Google Fonts API documentation

https://developers.google.com/fonts/docs/developer_api?hl=ja

`/environments/python.env`

```shell
GOOGLE_FONTS_API_KEY=<YOUR_API_KEY>
```

## List the web fonts you need

`config/webfonts.json`

```json
{
  "notosansjp": "Noto Sans JP",
  "notoserifjp": "Noto Serif JP"
}
```

## Generate fonts

```shell
$ docker-compose up
```
