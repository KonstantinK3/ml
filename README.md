#### Анаконда - создать и активировать окружение

```
conda env create
activate snippets_ml
```

#### Запуск Tensorboard 0.1.8 (из директории на уровень выше логов (keras_game_sales dir))

```
tensorboard --logdir=logs
```

#### Деактивировать и удалить окружение

```
deactivate snippets_ml
conda remove -y -n snippets_ml --all
```
