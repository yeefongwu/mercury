import json
from typing import Dict, Union, List, Optional, Set

class PremiumValidator:
    
    @staticmethod
    def _validate_breakdown(breakdown: Dict, seen_names: Set[str]) -> bool:
        name = breakdown.get("name")
        amount = breakdown.get("amount")
        
        if not (isinstance(name, str) or not (isinstance(amount, (int, float)))):
            return False
        #check duplicate breakdown 
        if name in seen_names:  
            return False
        
        seen_names.add(name)
        return True

    @staticmethod
    def _validate_alternative(alt: Dict, seen_alt_names: Set[str]) -> bool:
        name = alt.get("name")
        coverage_premium = alt.get("coveragePremium")
        coverage_value = alt.get("coverageValue")
        
        if not (isinstance(name, str) and isinstance(coverage_premium, (int, float)) and isinstance(coverage_value, str)):
            return False
        #check duplicate alternative
        if name in seen_alt_names:  
            return False
        
        seen_alt_names.add(name)
        
        # Validate breakdowns (with uniqueness check)
        breakdowns = alt.get("breakdowns", [])
        seen_bd_names = set()
        return all(
            PremiumValidator._validate_breakdown(b, seen_bd_names)
            for b in breakdowns
        )


    @staticmethod
    def validate_with_errors(payload: Union[Dict, str]) -> Optional[List[str]]:
        try:
            p = json.loads(payload) if isinstance(payload, str) else payload
            errors = []
            seen_bd_names = set()
            seen_alt_names = set()
            
            # Validate main fields
            if not isinstance(p.get("coverageName"), str):
                errors.append("Missing/invalid 'coverageName' (expected string)")
            if not isinstance(p.get("coveragePremium"), (int, float)):
                errors.append("Missing/invalid 'coveragePremium' (expected number)")
            if not isinstance(p.get("coverageValue"), str):
                errors.append("Missing/invalid 'coverageValue' (expected string)")
            
            # Validate breakdowns (check for duplicates)
            for i, bd in enumerate(p.get("breakdowns", [])):
                if not PremiumValidator._validate_breakdown(bd, seen_bd_names):
                    errors.append(f"Breakdown #{i+1} is invalid or has a duplicate name")
            
            # Validate alternatives (check for duplicates)
            for i, alt in enumerate(p.get("alternatives", [])):
                if not PremiumValidator._validate_alternative(alt, seen_alt_names):
                    errors.append(f"Alternative #{i+1} is invalid or has a duplicate name")
            
            return errors if errors else None
            
        except json.JSONDecodeError:
            return ["Invalid JSON format"]



