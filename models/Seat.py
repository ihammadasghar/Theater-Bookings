class Seat:
    def __init__(self, position: str, vip: bool, price: float) -> None:
        self.position = position
        self.vip = vip
        self.price = price