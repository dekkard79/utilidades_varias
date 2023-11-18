from rembg import remove
from PIL import Image

print("Inicio del programa")
input_path = str(input("Introduce nombre de fichero: "))
output_path = "salida"+input_path
inp = Image.open(input_path)
output = remove(inp)
output.save("output.png")
print("Fin del programa")