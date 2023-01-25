def Rumination():
    return PCS['I08']+PCS['I09']+PCS['I10']+PCS['I11']

def Magnification():
    return PCS['I06']+PCS['I07']+PCS['I13']

def Helplessness():
    return PCS['I01']+PCS['I02']+PCS['I03']+PCS['I04']+PCS['I05']+PCS['I12']

def Total():
    return Rumination() + Magnification() + Helplessness()


