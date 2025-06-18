"""Taxonomy processing functions for SNPraefentia."""

import logging
from ete3 import NCBITaxa

logger = logging.getLogger(__name__)

# Initialize NCBITaxa once at the module level
try:
    ncbi = NCBITaxa()
except Exception as e:
    logger.warning(f"Could not initialize NCBITaxa: {str(e)}")
    logger.warning("First-time users need to run 'from ete3 import NCBITaxa; ncbi = NCBITaxa()' to download the taxonomy database")
    ncbi = None

def get_taxid(species_name):
    """Get NCBI taxonomy ID for a species name.
    
    Args:
        species_name: Bacterial species name
        
    Returns:
        Taxonomy ID as an integer, or None if not found
    """
    if not ncbi:
        logger.error("NCBITaxa not initialized")
        return None
        
    try:
        name2taxid = ncbi.get_name_translator([species_name])
        if species_name in name2taxid:
            return name2taxid[species_name][0]
        else:
            logger.warning(f"No taxonomy ID found for {species_name}")
            return None
    except Exception as e:
        logger.warning(f"Error getting taxonomy ID: {str(e)}")
        return None