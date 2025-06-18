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
Working with NCBI taxonomy identifiers, it ensures precise species identification
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