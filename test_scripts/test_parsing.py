#!/usr/bin/env python
"""
Test the parsing logic manually
"""


# Test the parsing logic
def parse_address_input(address_input):
    address_input = address_input.strip()
    street = ""
    suburb = ""
    state = ""

    if "," in address_input:
        parts = address_input.split(",", 1)
        street = parts[0].strip()
        remainder = parts[1].strip() if len(parts) > 1 else ""
    elif "\t" in address_input:
        parts = address_input.split("\t", 1)
        street = parts[0].strip()
        remainder = parts[1].strip() if len(parts) > 1 else ""
    else:
        # Fallback: assume "street suburb state" format
        parts = address_input.rsplit(" ", 2)
        if len(parts) >= 2:
            street = parts[0].strip()
            suburb = parts[1].strip()
            if len(parts) >= 3:
                state = parts[2].strip()
        else:
            street = address_input
            suburb = ""
            state = ""

    # If we have a remainder, try to split it into suburb and state
    if "remainder" in locals() and remainder:
        remainder_parts = remainder.rsplit(" ", 1)
        if len(remainder_parts) >= 2:
            potential_state = remainder_parts[1].strip()
            # Check if the last part looks like a state abbreviation
            australian_states = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
            if potential_state.upper() in australian_states:
                suburb = remainder_parts[0].strip()
                state = potential_state.upper()
            else:
                # Not a state, treat whole remainder as suburb
                suburb = remainder
        else:
            suburb = remainder

    return street, suburb, state


# Test cases
test_cases = [
    "9 New Rd, Newtown WA",
    "123 Test St, Test Suburb",
    "14 Weil Avenue, Croydon Park NSW",
]

for test_input in test_cases:
    street, suburb, state = parse_address_input(test_input)
    print(f"Input: {test_input!r}")
    print(f"  Street: {street!r}")
    print(f"  Suburb: {suburb!r}")
    print(f"  State: {state!r}")
    print()
