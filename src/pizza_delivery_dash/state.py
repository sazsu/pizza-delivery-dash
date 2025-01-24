import enum


class State(enum.Enum):
    unknown = 'unknown'
    initializing = 'initializing'
    initialized = 'initialized'
    game_playing = 'game_playing'
    main_menu = 'main_menu'
    city = 'city'
    shop = 'shop'
    pizzeria = 'pizzeria'
    statistics = 'statistics'
    quitting = 'quitting'


class StateError(Exception):
    pass
