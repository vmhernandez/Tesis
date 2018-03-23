from Libreria_tesis import angle_calculation,angle_calculation2,angle_formatting

value=[200,500,442,415]

angle1=angle_calculation(value)

print("ANGLE 1")
for x in range(0,4):
    print(angle1[x])
    
angle2=angle_calculation2(value)

print("ANGLE 2")
for x in range(0,4):
    print(angle2[x])
    
angle3=angle_formatting(angle2)
print(angle3)