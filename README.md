# python-sam-app

## Tips

### 相対importを使う場合は自分がパッケージに属している必要がある

* bmonster.scrapingでは相対importは使えない
    * bmonsterがルートディレクトリになるためパッケージ扱いにならない
* bmonster.app.scrapingなら相対importが使える
    * scrapingモジュールがappパッケージに属しているため 

## BmonsterApplication

### BmonsterRequirementsLayer

```shell
pipenv requirements > bmonster/requirements/requirements.txt
sam build BmonsterRequirementsLayer
```

### BmonsterScrapingFunction

```shell
sam local invoke --docker-network python-sam-app_default BmonsterScrapingFunction
```

### BmonsterScheduleApiFunction

```shell
sam local invoke --docker-network python-sam-app_default BmonsterScheduleApiFunction -e events/event.json
sam local start-api --docker-network python-sam-app_default
```

### BmonsterPerformerApiFunction

```shell
sam local invoke --docker-network python-sam-app_default BmonsterPerformerApiFunction -e events/event.json
sam local start-api --docker-network python-sam-app_default
```

### BmonsterProgramApiFunction

```shell
sam local invoke --docker-network python-sam-app_default BmonsterProgramApiFunction -e events/event.json
sam local start-api --docker-network python-sam-app_default
```

### BmonsterProgramReviewApiFunction

```shell
sam local invoke --docker-network python-sam-app_default BmonsterProgramReviewApiFunction -e events/BmonsterProgramReviewApiFunction/getEvent.json
sam local invoke --docker-network python-sam-app_default BmonsterProgramReviewApiFunction -e events/BmonsterProgramReviewApiFunction/postEvent.json
sam local start-api --docker-network python-sam-app_default
```
