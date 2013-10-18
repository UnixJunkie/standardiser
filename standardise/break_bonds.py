"""Break bonds to Group I and II metals"""

########################################################################

# Module imports...

from __future__ import print_function

import logging; logger = logging.getLogger(__name__)

from collections import defaultdict

from rdkit import Chem

########################################################################

# Module configuration...

bonds_to_break = [("[Li,Na,K,Mg,Ca]-[#7,#8,#16]", 1), ("[Mg,Ca]=N", 2)] # SMARTS pattern, charge increment

########################################################################

# Module initialization...

bonds_to_break = [(Chem.MolFromSmarts(smarts), charge_incr) for smarts, charge_incr in bonds_to_break]

########################################################################

def apply(mol):

    charge_added = defaultdict(int)

    n = 0

    for pattern, charge_incr in bonds_to_break:

        idx_pairs = mol.GetSubstructMatches(pattern)

        ed_mol = Chem.EditableMol(mol)

        for i, j in idx_pairs:

            ed_mol.RemoveBond(i, j)

            n += 1

        mol = ed_mol.GetMol()

        for i, j in idx_pairs:

            atom = mol.GetAtomWithIdx(i)
            atom.SetFormalCharge(atom.GetFormalCharge() + charge_incr)

            charge_added[i] += charge_incr

            atom = mol.GetAtomWithIdx(j)
            atom.SetFormalCharge(atom.GetFormalCharge() - charge_incr)

            charge_added[j] -= charge_incr

    Chem.SanitizeMol(mol)

    logger.debug("Broke {} bonds to Group I and II metals".format(n))

    return mol ###, charge_added

# apply

########################################################################
# End
########################################################################