from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """Strategy Pattern - Narx strategiyasi interface"""
    
    @abstractmethod
    def calculate_total(self, bill) -> float:
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        pass

class StandardPricing(PricingStrategy):
    """Standart narx"""
    
    def calculate_total(self, bill) -> float:
        return bill.subtotal
    
    def get_strategy_name(self) -> str:
        return "Standard Pricing"

class HappyHourPricing(PricingStrategy):
    """Happy Hour - 20% chegirma"""
    
    DISCOUNT = 0.20
    
    def calculate_total(self, bill) -> float:
        return bill.subtotal * (1 - self.DISCOUNT)
    
    def get_strategy_name(self) -> str:
        return f"Happy Hour Pricing ({int(self.DISCOUNT*100)}% off)"

class LoyaltyCardPricing(PricingStrategy):
    """Sodiqlik kartasi - 10% chegirma + bepul ichimlik"""
    
    DISCOUNT = 0.10
    
    def calculate_total(self, bill) -> float:
        return bill.subtotal * (1 - self.DISCOUNT)
    
    def get_strategy_name(self) -> str:
        return f"Loyalty Card Pricing ({int(self.DISCOUNT*100)}% off + free drink)"

class WeekendSurchargePricing(PricingStrategy):
    """Dam olish kunlari - 10% qo'shimcha"""
    
    SURCHARGE = 0.10
    
    def calculate_total(self, bill) -> float:
        return bill.subtotal * (1 + self.SURCHARGE)
    
    def get_strategy_name(self) -> str:
        return f"Weekend Surcharge (+{int(self.SURCHARGE*100)}%)"

class PricingEngine:
    """Context - Strategiyani runtime'da o'zgartirish"""
    
    def __init__(self, strategy: PricingStrategy = None):
        self._strategy = strategy or StandardPricing()
    
    @property
    def strategy(self) -> PricingStrategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, new_strategy: PricingStrategy):
        self._strategy = new_strategy
    
    def calculate_total(self, bill) -> float:
        """Joriy strategiya bilan narx hisoblash"""
        return self._strategy.calculate_total(bill)
    
    def get_current_strategy_name(self) -> str:
        return self._strategy.get_strategy_name()
