# games package — exposes all six game classes
from .slot_machine import SlotMachine
from .aviator import AviatorGame
from .double import DoubleGame
from .crash_dice import CrashDice
from .blackjack import Blackjack
from .roulette import Roulette
from .coin_flip import CoinFlip

__all__ = ["SlotMachine", "AviatorGame", "DoubleGame", "CrashDice", "Blackjack", "Roulette", "CoinFlip"]
