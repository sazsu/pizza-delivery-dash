import enum


class State(enum.Enum):
    unknown = 'unknown'
    initializing = 'initializing'
    initialized = 'initialized'
    game_playing = 'game_playing'
    main_menu = 'main_menu'
    inside_city = 'inside_city'
    inside_shop = 'inside_shop'
    inside_pizzeria = 'inside_pizzeria'
    delivering_pizza = 'delivering_pizza'
    showing_statistics = 'showing_statistics'
    quitting = 'quitting'


class StateError(Exception):
    pass
