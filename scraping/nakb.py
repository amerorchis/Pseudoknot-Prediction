"""
Verify that the NAKB structure contains a pseudoknot.
"""

import requests

def contains_pseudoknot(nakb_id: str) -> bool:
    """
    Takes an NAKB id and returns True if the structure has a pseudoknot, else False.
    """
    url = f"https://www.nakb.org/x3dssr/{nakb_id}_1.json"
    r = requests.get(url, timeout=5)
    try:
        data = r.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f'DBN not found for {nakb_id}.', e)
        return None

    dbn = data['dbn']['all_chains']['sstr']

    # Check if any of the pseudoknot characters are in dot bracket notation.
    for i in r'[]{}<>':
        if i in dbn:
            return True

    return False

if __name__ == "__main__":
    assert contains_pseudoknot('7MKY') is True
    assert contains_pseudoknot('3SJ2') is False
