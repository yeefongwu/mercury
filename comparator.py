import json
from typing import Dict, List, Union

class PremiumComparator:
    """Compares two Premium payloads for equivalence."""
    
    @staticmethod
    def compare_breakdowns(b1: List[Dict], b2: List[Dict], tolerance: float) -> bool:
        """Compare two lists of breakdowns (order-independent)"""
        if len(b1) != len(b2):
            return False
            
        sorted_b1 = sorted(b1, key=lambda x: x["name"])
        sorted_b2 = sorted(b2, key=lambda x: x["name"])
        
        return all(
            (bd1["name"] == bd2["name"]) and 
            (abs(bd1["amount"] - bd2["amount"]) <= tolerance)
            for bd1, bd2 in zip(sorted_b1, sorted_b2)
        )

    @staticmethod
    def compare_alternatives(a1: List[Dict], a2: List[Dict], tolerance: float) -> bool:
        """Compare two lists of alternatives (order-independent)"""
        if len(a1) != len(a2):
            return False
            
        sorted_a1 = sorted(a1, key=lambda x: x["name"])
        sorted_a2 = sorted(a2, key=lambda x: x["name"])
        
        return all(
            (alt1["name"] == alt2["name"]) and
            (alt1["coverageValue"] == alt2["coverageValue"]) and
            (abs(alt1["coveragePremium"] - alt2["coveragePremium"]) <= tolerance) and
            PremiumComparator.compare_breakdowns(alt1.get("breakdowns", []), alt2.get("breakdowns", []), tolerance)
            for alt1, alt2 in zip(sorted_a1, sorted_a2)
        )

    @staticmethod
    def are_equal(
        payload1: Union[Dict, str],
        payload2: Union[Dict, str],
        tolerance: float = 0.01
    ) -> bool:
        """Main comparison method"""
        try:
            p1 = json.loads(payload1) if isinstance(payload1, str) else payload1
            p2 = json.loads(payload2) if isinstance(payload2, str) else payload2
            
            return (
                (p1["coverageName"] == p2["coverageName"]) and
                (p1["coverageValue"] == p2["coverageValue"]) and
                (abs(p1["coveragePremium"] - p2["coveragePremium"]) <= tolerance) and
                PremiumComparator.compare_breakdowns(p1.get("breakdowns", []), p2.get("breakdowns", []), tolerance) and
                PremiumComparator.compare_alternatives(p1.get("alternatives", []), p2.get("alternatives", []), tolerance)
            )
        except (KeyError, json.JSONDecodeError, TypeError):
            return False


if __name__ == "__main__":
    with open("premium_1.json", "r") as f1, open("p1_same.json", "r") as f2:
        payload1 = json.load(f1)
        payload2 = json.load(f2)
    
    print("Are equal?", PremiumComparator.are_equal(payload1, payload2))