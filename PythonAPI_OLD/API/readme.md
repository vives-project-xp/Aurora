# API

> **All data should be send in a json format**

You can change the ledstrip by sending http request to **http://aurora.local:5500/**

## Toggle ledstrip
> http request: /toggle

## Set color
> http request: /color

```
{"red": [0-255] ,"green": [0-255] ,"blue": [0-255], "alpha": [0-255]}
```

## Select preset
> http request: /preset

```
{"ps": [0-10]}
```