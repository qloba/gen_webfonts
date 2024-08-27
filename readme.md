# Webfont generator

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
