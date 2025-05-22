# Read Me
# The directoy include three files i-e input.xlsx, output.xlsx and Source_Code.ipynb
# The input file include the SNPs and its relevant information which need to be prioritized
# The output file include the calculated priorizted score of SNPs along with some additional information
# The Source_Code file include the main python based code that is used to prioritized SNPs

# End to End prioritizartion of SNPs from a list, follows 13 steps which is executed sequentially

# Names of all the packages and dependencies that need to be installed are mentioned in the beginning of the source code plus its successful execution is also mentioned accordingly

# NOTE: There is a specific database that need to be retrived by the user once they are using this for the first time. Total size of the database is 600+ MB (its a one time retrieval). This need to be mentioned to the user. The database include taxa ids of bacterial species. The code used for this retrieval is mentioned as follow;

# pip install ete3
# from ete3 import NCBITaxa

# The latter execution of the code is mentioned in the recorded video (SNPs priorization tutorial.mp4)