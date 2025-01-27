def Stess(tc):
    return (tc.DASS['I01']+tc.DASS['I06']+tc.DASS['I08']+tc.DASS['I11']+tc.DASS['I12']+tc.DASS['I14']+tc.DASS['I18']+
            tc.DASS['I22']+tc.DASS['I27']+tc.DASS['I29']+tc.DASS['I32']+tc.DASS['I33']+tc.DASS['I35']+tc.DASS['I39'])

def Anxiety(tc):
    return (tc.DASS['I02']+tc.DASS['I04']+tc.DASS['I07']+tc.DASS['I09']+tc.DASS['I15']+tc.DASS['I19']+tc.DASS['I20']+
            tc.DASS['I23']+tc.DASS['I25']+tc.DASS['I28']+tc.DASS['I30']+tc.DASS['I36']+tc.DASS['I40']+tc.DASS['I41'])

def Depresion(tc):
    return (tc.DASS['I03']+tc.DASS['I05']+tc.DASS['I10']+tc.DASS['I13']+tc.DASS['I16']+tc.DASS['I17']+tc.DASS['I21']+
            tc.DASS['I24']+tc.DASS['I26']+tc.DASS['I31']+tc.DASS['I34']+tc.DASS['I37']+tc.DASS['I38']+tc.DASS['I42'])


