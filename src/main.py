from pizza_delivery_dash.game import PizzaDeliveryDash


def run_game() -> None:
    game = PizzaDeliveryDash.create()
    game.loop()


if __name__ == '__main__':
    try:
        run_game()
    except Exception as e:
        print(f'Exception occured: {e}')
