import calculadora.calculadora as calculadora
if __name__ =="__main__":
    num=float(input("Ingrese un número: "))
    otro_numero=float(input("Ingrese otro número: "))
    operacion=input("Ingrese una operacion(A: suma, B: resta, C: multiplicacion, D: division): ")
    if(operacion=="A"):
        print(calculadora.suma(num,otro_numero))
    elif(operacion=="B"):
        print(calculadora.resta(num,otro_numero))
    elif(operacion=="C"):
       print(calculadora.multiplicacion(num,otro_numero))
    elif(operacion=="D"):
        print(calculadora.division(num,otro_numero))
    else:
        print("operacion invalida")


   
    