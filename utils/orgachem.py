#!/usr/bin/python3
class OrgaChem():
    def __init__(self):
        self.alkane = 'R-CH2-CH2-R'
        self.alkene = 'R-CH=CH-R'
        self.alkyne = 'R-C≡C-R'
        self.alcohol = 'R-OH'
        self.ether = 'R-O-R\''
        self.ketone = 'R-C=O\n   \\R\''
        self.aldehyde = 'R-C=O\n   \\H'
        self.carboxylic_acid = 'R-C=O\n   \\OH'
        self.ester = 'R-C=O\n   \\O-R\''
        self.amine = 'R-NH2'
        self.amide = 'R-C=O\n   \\NH2'

        self.compounds = [
        ['alkane', 'alcane', self.alkane],
        ['alkene', 'alcène', self.alkene],
        ['alkyne', 'alcyne', self.alkyne],
        ['alcohol', 'alcool', self.alcohol],
        ['ether', 'éther-oxyde', 'éther', self.ether],
        ['ketone', 'cétone', self.ketone],
        ['aldehyde', 'aldéhyde', self.aldehyde],
        ['carboxylic acid', 'acide carboxylique', self.carboxylic_acid],
        ['ester', 'ester', self.ester],
        ['amine', 'amine', self.amine],
        ['amide', 'amide', self.amide]]
