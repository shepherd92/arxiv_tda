#!/usr/bin/env python
"""Represent enumerated types for Arxiv data set categories."""

from enum import Enum

# pylint: disable=invalid-name

class ArxivCategory(Enum):
    """Categories and their representation."""

    math_AC = 'math.AC'
    math_AG = 'math.AG'
    math_AP = 'math.AP'
    math_AT = 'math.AT'
    math_CA = 'math.CA'
    math_CO = 'math.CO'
    math_CT = 'math.CT'
    math_CV = 'math.CV'
    math_DG = 'math.DG'
    math_DS = 'math.DS'
    math_FA = 'math.FA'
    math_GM = 'math.GM'
    math_GN = 'math.GN'
    math_GR = 'math.GR'
    math_GT = 'math.GT'
    math_HO = 'math.HO'
    math_IT = 'math.IT'
    math_KT = 'math.KT'
    math_LO = 'math.LO'
    math_MG = 'math.MG'
    math_MP = 'math.MP'
    math_NA = 'math.NA'
    math_NT = 'math.NT'
    math_OA = 'math.OA'
    math_OC = 'math.OC'
    math_PR = 'math.PR'
    math_QA = 'math.QA'
    math_RA = 'math.RA'
    math_RT = 'math.RT'
    math_SG = 'math.SG'
    math_SP = 'math.SP'
    math_ST = 'math.ST'
    ALL = ''

# pylint: enable=invalid-name
