class Player:
    def __init__(self, position, stack_size, is_away, cards=None):
        self.position = position
        self.cards = cards or []
        self.stack_size = stack_size
        self.is_away = is_away
        self.relative_position = None

    @classmethod
    def with_cards(cls, position, stack_size, is_away, cards):
        return cls(position, stack_size, is_away, cards)

    def set_relative_position(self, dealer_position, active_players):
        if self.is_away:
            self.relative_position = 'Away'
            return

        # Adjust position based on active players only
        active_positions = [player.position for player in active_players if not player.is_away]
        effective_position = active_positions.index(self.position)
        distance_from_button = (effective_position - active_positions.index(dealer_position)) % len(active_positions)

        if distance_from_button == 0:
            self.relative_position = 'Dealer'
        elif distance_from_button == 1:
            self.relative_position = 'Small Blind'
        elif distance_from_button == 2:
            self.relative_position = 'Big Blind'
        elif distance_from_button <= 3:
            self.relative_position = 'Early Position'
        elif distance_from_button <= 6:
            self.relative_position = 'Middle Position'
        else:
            self.relative_position = 'Late Position'

    def __repr__(self):
        return f"Player(position={self.position}, cards={self.cards}, stack_size={self.stack_size}, is_away={self.is_away}, relative_position={self.relative_position})"
