import pandas as pd

csv = pd.read_csv('data.csv')
#excel = pd.read_excel('dataset.xlsm')

csv = csv.sort_values(by=['brand'])

print(csv['brand'].value_counts().to_string())

''' becomes unknown
plastic
can
metal
beer
cup
paper
papercup
aluminium
aluminum
plasticbottle
bag
foil
packaging
wrapper
bottlecap
chemicals
'''

'''
kitakt = kitkat
autodrup = autodrop
export bier = export
soda = dubbel friss
'''

''' which cola brand?
cola
'''