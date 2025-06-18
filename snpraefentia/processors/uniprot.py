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
"""UniProt data processing module.

This module serves as the interface between SNPraefentia and the UniProt protein
database. It performs protein identification by searching the UniProt database using gene names and species information.
"""

import logging
import requests
import pandas as pd
from io import StringIO

logger = logging.getLogger(__name__)

def search_uniprot(gene, species_taxid, target_length, tolerance=50):
    """Search UniProt for a gene from a specific species.
    
    Args:
        gene: Gene name
        species_taxid: NCBI Taxonomy ID
        target_length: Expected protein length
        tolerance: Length tolerance for matching
        
    Returns:
        UniProt ID as a string, or None if not found
    """
    if not gene or not species_taxid or not target_length:
        return None
        
    try:
        query = f'gene:{gene} AND organism_id:{species_taxid}'
        url = f"https://rest.uniprot.org/uniprotkb/search?query={query}&fields=accession,gene_names,organism_name,length&format=tsv&size=50"
        
        logger.debug(f"Querying UniProt: {url}")
        response = requests.get(url)
        
        if response.status_code != 200:
            logger.warning(f"UniProt request failed: {response.status_code}")
            return None
            
        df_results = pd.read_csv(StringIO(response.text), sep='\t')
        
        if df_results.empty:
            logger.debug(f"No UniProt results for {gene} (taxid: {species_taxid})")
            return None
            
        df_results['Length_diff'] = abs(df_results['Length'] - target_length)
        close_matches = df_results[df_results['Length'].between(target_length - tolerance, target_length + tolerance)]
        
        if not close_matches.empty:
            best_match = close_matches.sort_values('Length_diff').iloc[0]['Entry']
            logger.debug(f"Found UniProt match: {best_match}")
            return best_match
        else:
            logger.debug(f"No suitable length match for {gene} (target: {target_length})")
            return None
            
    except Exception as e:
        logger.warning(f"Error searching UniProt: {str(e)}")
        return None

def check_domain_position(uniprot_id, mutated_position):
    """Check if a mutated position is within a protein domain.
    
    Args:
        uniprot_id: UniProt ID
        mutated_position: Position of the mutation
        
    Returns:
        1 if within a domain, 0 otherwise
    """
    if pd.isna(uniprot_id) or pd.isna(mutated_position):
        return 0
        
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
        logger.debug(f"Querying UniProt for domains: {url}")
        
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning(f"UniProt domain request failed: {response.status_code}")
            return 0
            
        data = response.json()
        features = data.get('features', [])
        
        for feature in features:
            if feature.get('type') == 'Domain':
                begin = feature.get('location', {}).get('start', {}).get('value')
                end = feature.get('location', {}).get('end', {}).get('value')
                
                if begin is not None and end is not None:
                    if int(begin) <= int(mutated_position) <= int(end):
                        logger.debug(f"Position {mutated_position} is within domain {begin}-{end}")
                        return 1
                        
        logger.debug(f"Position {mutated_position} is not within any domain")
        return 0
        
    except Exception as e:
        logger.warning(f"Error checking domain position: {str(e)}")
        return 0