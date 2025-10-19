import datetime

class Proveedor:
    def __init__(self, nombre, telefono, correo, direccion, id=None, activo=True, fecha_ingreso=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.activo = activo
        if fecha_ingreso is None:
            self.fecha_ingreso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.fecha_ingreso = fecha_ingreso

    @classmethod
    def desde_dicc(cls, datos):
        return cls(
            id=datos['ID'],
            nombre=datos['Nombre'],
            telefono=datos['Telefono'],
            correo=datos['Correo'],
            direccion=datos['Direccion'],
            activo=datos['Activo', True],
            fecha_ingreso=datos.get('Fecha_ingreso')
        )

    def a_dicc(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "correo": self.correo,
            "direccion": self.direccion,
            "activo": self.activo,
            "fecha_ingreso": self.fecha_ingreso
        }