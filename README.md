# Pizza Delivery Dash

## Об игре

Играйте за персонажа, работающего доставщиком пиццы. Следите за временем прохождения уровня, собирайте необходимые ингредиенты, готовьте пиццу, доставляйте ее клиентам.

## Жанр игры

Аркада

## Сюжет

Вы устроились на работу в местную пиццерию, однако ваша работа не совсем обычная. Вам придется столкнуться с препятствиями и пытаться заслужить доверие руководства, чтобы вас не уволили. Из-за нехватки финансирования и кадров, вам приходится совмещать работу повара и доставщика пиццы. Ингредиенты для пиццы вам тоже приходится собирать самостоятельно. Постарайтесь всё успеть, чтобы клиенты остались довольны.

## Пререквизиты

- [git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) (>=3.12)
- [uv](https://docs.astral.sh/uv/) (опционально)

## Быстрый старт

#### Клонируйте проект

```shell
git clone https://github.com/sazsu/pizza-delivery-dash.git
```

#### Перейдите в директорию проекта

```shell
cd pizza-delivery-dash
```

#### Установите зависимости (uv)

##### С dev зависимостями

```shell
uv sync --all-extras
```

##### Без dev зависимостей

```shell
uv sync --no-dev
```

#### Установите зависимости (pip)

##### Создайте и активируйте виртуальное окружение

```shell
python -m venv .venv

# Для Linux и macOS
source .venv/bin/activate

# Для Windows
.venv\Scripts\activate
```

##### Установите зависимости из requirements.txt

```shell
python -m pip install -r requirements.txt
```

#### Запустите проект

##### uv

```shell
uv run python src/main.py
```

##### python

```shell
python src/main.py
```

## Презентация

[figma](https://www.figma.com/deck/wVk7DbWxfKL2eawT7rHCsR/PDD-presentation?node-id=2-25&t=T0U2XQP8z4YqvxbW-1)

## Благодарности

[Pico-8 City](https://kenney.nl/assets/pico-8-city), лицензировано на условиях [CC0 1.0 Universal](https://creativecommons.org/public-domain/cc0/)

[Pixel food!](https://henrysoftware.itch.io/pixel-food), лицензировано на условиях [CC0 1.0 Universal](https://creativecommons.org/public-domain/cc0/)

[Super Market 2D Tileset](https://blockydk.itch.io/supermarket-tileset), сделанный Blocky, лицензировано на условиях [CC BY](https://creativecommons.org/licenses/by/4.0/)

## Лицензия

MIT
