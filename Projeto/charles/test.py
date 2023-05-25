from sdp_data import foods

diet_plan = {}
fr = [0, 0, 0, 0, 0.6, 0, 0, 0.6, 0, 0, 0.1, 0, 0.3, 0.4, 0.9, 0.5, 0, 0.3, 0, 1.0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0.4, 0, 0, 0.9, 0.8, 0.3, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0.2, 0.1, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.3, 0, 0, 0, 0, 0, 0, 0.5, 0.6, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 1.0, 0, 0]
#for i in foods.index.tolist():
 #   value = fr.pop(0)
  #  diet_plan[i] = value
for i, q, u in zip(foods.index.tolist(), foods['quantity'].tolist(), foods['unit'].tolist()):
    value = f"{fr[i] * q} {u}"
    diet_plan[i] = value

print(diet_plan)

filtered_diet_plan = {key: value for key, value in diet_plan.items() if not value.startswith('0.0')}
print(filtered_diet_plan)
'''
def verify_macros():
    return True, [0, 1, 2]

print(verify_macros()[1])

fr = [0, 0, 0, 0, 0.6, 0, 0, 0.6, 0, 0, 0.1, 0, 0.3, 0.4, 0.9, 0.5, 0, 0.3, 0, 1.0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0.4, 0, 0, 0.9, 0.8, 0.3, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0.2, 0.1, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.3, 0, 0, 0, 0, 0, 0, 0.5, 0.6, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 1.0, 0, 0]
print(len(fr))
for i in enumerate(foods.index):
    print(i)'''