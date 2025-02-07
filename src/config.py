class Config:
    FPS = 60
    TILE_SIZE = 8
    PLAYER_VELOCITY = 2  # pixels/step
    PLAYER_NAME = 'Игрок №1'
    BUILDING_LAYER = frozenset(
        [
            'a',
            'b',
            'c',
            'd',
            'i',
            'j',
            'k',
            'l',
            'lwq',
            'wq',
            'rwq',
            'p',
        ]
    )


def dbg(msg: str) -> None:
    print(f'[d] {msg}')
