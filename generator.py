import json
import random
from typing import List, Set
from uuid import uuid4
from models import Premium, PremiumBreakdown, AlternativePremium

class PremiumGenerator:
    
    @staticmethod
    def generate_unique_breakdown(existing_names: Set[str]) -> PremiumBreakdown:
        """Generate a breakdown with a unique name (avoids duplicates)."""
        breakdown_types = ["Base Premium", "Tax", "Fee", "Discount", "Surcharge"]
        available_types = [b for b in breakdown_types if b not in existing_names]
        
        if not available_types:
            return None  # No more unique breakdowns possible
        
        chosen_type = random.choice(available_types)
        price = round(random.uniform(10, 1000), 2)
        
        if chosen_type == "Base Premium":
            price = round(random.uniform(500, 3000), 2)  # Higher range for base premium
        
        return PremiumBreakdown(name=chosen_type, amount=price)

    @staticmethod
    def generate_alternative(existing_alternative_names: Set[str]) -> AlternativePremium:
        """Generate an alternative with a unique name (avoids duplicates)."""
        scenarios = ["High-Deductible", "Low-Cost", "Premium", "Standard"]
        available_scenarios = [s for s in scenarios if f"{s} Option" not in existing_alternative_names]
        
        if not available_scenarios:
            return None  # No more unique alternatives possible
        
        chosen_scenario = random.choice(available_scenarios)
        alt_name = f"{chosen_scenario} Option"
        
        # Generate unique breakdowns for this alternative
        alt_breakdowns = []
        used_breakdown_names = set()
        
        for _ in range(random.randint(1, 4)):
            breakdown = PremiumGenerator.generate_unique_breakdown(used_breakdown_names)
            if not breakdown:
                break  # No more unique breakdowns possible
            alt_breakdowns.append(breakdown)
            used_breakdown_names.add(breakdown.name)  # Access field via attribute (not dict key)
        
        return AlternativePremium(
            name=alt_name, 
            coveragePremium=round(random.uniform(300, 5000), 2),
            coverageValue=f"${random.randint(500, 2000)} deductible",
            breakdowns=alt_breakdowns
        )
        
    @staticmethod
    def generate_premium() -> Premium:
        """Generate a complete premium payload with no duplicates."""
        coverages = ["Auto", "Home", "Life", "Health", "Travel"]
        
        # Generate main premium breakdowns
        main_breakdowns = []
        used_breakdown_names = set()
        
        for _ in range(random.randint(2, 5)):
            breakdown = PremiumGenerator.generate_unique_breakdown(used_breakdown_names)
            if not breakdown:
                break  # No more unique breakdowns possible
            main_breakdowns.append(breakdown)
            used_breakdown_names.add(breakdown.name)  # Access field via attribute
        
        # Generate alternatives (ensuring no duplicates)
        alternatives = []
        used_alternative_names = set()
        
        for _ in range(random.randint(1, 3)):
            alternative = PremiumGenerator.generate_alternative(used_alternative_names)
            if not alternative:
                break  # No more unique alternatives possible
            alternatives.append(alternative)
            used_alternative_names.add(alternative.name)  # Access field via attribute
        
        return Premium(
            id=str(uuid4()),
            coverageName=f"{random.choice(coverages)} Insurance",
            coveragePremium=round(random.uniform(500, 10000), 2),
            coverageValue=f"${random.randint(250, 1500)} deductible",
            breakdowns=main_breakdowns,
            alternatives=alternatives
        )

if __name__ == "__main__":
    premium_data = PremiumGenerator.generate_premium()
    with open("premiums.json", "w") as json_file:
        json.dump(premium_data.dict(), json_file, indent=2)  # Convert Pydantic model to dict before saving