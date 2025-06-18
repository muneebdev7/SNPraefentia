# Copyright 2025 SNPraefentia Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Taxonomy processing module.

This module forms the taxonomic foundation of the SNPraefentia analysis pipeline.
Working with NCBI taxonomy identifiers, it ensures precise specie identification
throughout the analysis process.
"""

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

def validate_specie_name(specie_name):
    """Validate if a specie name exists in the NCBI taxonomy database.
    
    Args:
        specie_name: Bacterial specie name to validate
        
    Returns:
        bool: True if specie exists, False otherwise
    """
    if not ncbi:
        logger.error("NCBITaxa not initialized")
        return False
        
    try:
        name2taxid = ncbi.get_name_translator([specie_name])
        return specie_name in name2taxid
    except Exception as e:
        logger.error(f"Error validating specie name: {str(e)}")
        return False

def get_taxid(specie_name):
    """Get NCBI taxonomy ID for a specie name.
    
    Args:
        specie_name: Bacterial specie name
        
    Returns:
        Taxonomy ID as an integer, or None if not found
    """
    if not ncbi:
        logger.error("NCBITaxa not initialized")
        return None
        
    try:
        name2taxid = ncbi.get_name_translator([specie_name])
        if specie_name in name2taxid:
            return name2taxid[specie_name][0]
        logger.warning(f"No taxonomy ID found for {specie_name}")
        return None
    except Exception as e:
        logger.error(f"Error getting taxonomy ID: {str(e)}")
        return None