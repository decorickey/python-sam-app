# python-sam-app

## Tips

### 相対importを使う場合は自分がパッケージに属している必要がある

* bmonster.scrapingでは相対importは使えない
    * bmonsterがルートディレクトリになるためパッケージ扱いにならない
* bmonster.app.scrapingなら相対importが使える
    * scrapingモジュールがappパッケージに属しているため 

## BmonsterApplication

```shell
pipenv requirements > bmonster/requirements.txt
```

### BmonsterScrapingFunction

```shell
sam build BmonsterScrapingFunction
sam local invoke --docker-network python-sam-app_default BmonsterScrapingFunction
```

### BmonsterScheduleApiFunction

```shell
sam build BmonsterScheduleApiFunction
sam local invoke --docker-network python-sam-app_default BmonsterScheduleApiFunction -e events/event.json
sam local start-api --docker-network python-sam-app_default
```
