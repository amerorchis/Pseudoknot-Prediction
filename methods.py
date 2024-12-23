"""
Define functions to predict pseudoknots with knotfold, pknotsrg, probknot, knotty, pknots.
"""

import subprocess
import tempfile
from Sequence import Sequence
from KnotFold.KnotFold import knotfold
from Method import Method

def knotfold_method(seq_obj: Sequence):
    """
    I had to re-write the output for knotfold because it wasn't in a useful format, so I also just
    had it imported as a python function and directly return a bool.
    """
    return knotfold(seq_obj.fasta_file)

def pknotsrg_method(seq_obj: Sequence):
    """
    Make a pseudoknot presence prediction with pknotsrg.
    Pseudoknots show up as [ or { in dot bracket notation (dbn).
    """
    fasta = seq_obj.raw_seq
    dbn = subprocess.run(["pknotsRG-mfe", fasta], capture_output=True, text=True, check=True, timeout=300).stdout
    assert dbn
    return '[' in dbn or '{' in dbn

def probknot_method(seq_obj: Sequence):
    """
    Make a pseudoknot presence prediction with probknot.
    """
    fasta = seq_obj.fasta_file

    # Create a temporary file to hold the ct output. Nesting is required because the file
    # is deleted when the context manager closes.
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete_on_close=False) as ct_file:
        ct_path = ct_file.name
        ct_file.close()

        subprocess.run(['ProbKnot', '--sequence', fasta, ct_path], capture_output=True, check=True, timeout=300)

        # Create a temporary file to hold the dot file output.
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete_on_close=False) as dot_file:
            dot_path = dot_file.name
            dot_file.close()

            # Convert the ct output to a dot file.
            subprocess.run(["ct2dot", ct_path, '1', dot_path], capture_output=True, check=True, timeout=300)

            # Read the dot file.
            with open(dot_path, 'r', encoding='utf-8') as dot:
                dbn = dot.read()

    # Pseudoknots show up as < in dot bracket notation (dbn).
    dbn = ''.join(dbn.split('\n')[2:])
    return '<' in dbn

def knotty_method(seq_obj: Sequence):
    """
    Make a pseudoknot presence prediction with knotty.
    Pseudoknots show up as [ or { in dot bracket notation (dbn).
    """
    fasta = seq_obj.raw_seq
    dbn = subprocess.run(["knotty", fasta], capture_output=True, text=True, check=True, timeout=300).stdout
    assert dbn
    return '[' in dbn or '{' in dbn

def pknots_method(seq_obj: Sequence):
    """
    Make a pseudoknot presence prediction with pknots.
    """
    fasta = seq_obj.fasta_file

    # Temporary file to hold ct output.
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete_on_close=False) as ct_file:
        ct_file_path = ct_file.name
        ct_file.close()

        # Make prediction and store it in ct file.
        subprocess.run(["pknots", '-kg', fasta, ct_file_path], capture_output=True, check=True, timeout=300)

        # Reopen the file to read its content
        with open(ct_file_path, 'r', encoding='utf-8') as temp_file:
            ct_raw = temp_file.read()

    # Alter the ct file so that it fits the ct2dot format.
    ct = ct_raw.split('\n')[4:]
    header = [str(seq_obj.seq_length)]
    header.extend(ct)

    # Write formatted ct data to a new ct file
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete_on_close=False) as ct_file_corrected:
        ct_corrected_path = ct_file_corrected.name
        ct_file_corrected.write('\n'.join(header))
        ct_file_corrected.close()

        # Open a dot file to store output
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete_on_close=False) as dot_file:
            dot_path = dot_file.name  # Store the path before closing
            dot_file.close()

            subprocess.run(["ct2dot", ct_corrected_path, '1', dot_path], capture_output=True, check=True, timeout=300)

            # Open the dot file to read the results
            with open(dot_path, 'r', encoding='utf-8') as dot:
                dbn = dot.read()

    # Pseudoknot signified by < in dbn.
    dbn = ''.join(dbn.split('\n')[2:])
    return '<' in dbn

def knot2shabby_method(seq_obj: Sequence):
    """
    Check what kingdom/virus the RNA is from and use the method that performs best on that group.
    """
    by_kingdom = {
        'Unknown Kingdom': knotty_method,
        'Viruses': knotty_method,
        'Bacteria': knotfold_method,
        'Eukaryota': knotfold_method,
    }

    method = by_kingdom[seq_obj.kingdom]
    return method(seq_obj)

debug = False
methods = [
    Method('knotfold', knotfold_method, debug=debug),
    Method('pknots', pknots_method, debug=debug),
    Method('pknotsrg', pknotsrg_method, debug=debug),
    Method('probknot', probknot_method, debug=debug),
    Method('knotty', knotty_method, debug=debug),
    Method('knot2shabby', knot2shabby_method, debug=debug)
    ]
