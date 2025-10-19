from datetime import datetime

class Envio:
    def __init__(self, proveedor, cliente, destino, estado, numero_seguimiento, fecha_entrega, fecha_ingreso=None, id=None):
        self.id = id
        self.proveedor = proveedor
        self.cliente = cliente
        self.destino = destino
        self.estado = estado
        self.numero_seguimiento = numero_seguimiento
        self.fecha_entrega = fecha_entrega
        if fecha_ingreso is None:
            self.fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.fecha_ingreso = fecha_ingreso

    def a_dicc(self):
        # Convierte el envío a diccionario para la base de datos
        return {
            'id': self.id,
            'proveedor': self.proveedor,
            'cliente': self.cliente,
            'destino': self.destino,
            'estado': self.estado,
            'numero_seguimiento': self.numero_seguimiento,
            'fecha_entrega': self.fecha_entrega,
            'fecha_ingreso': self.fecha_ingreso
        }

    @classmethod
    def desde_dicc(cls, data):
        # Crea un Envio desde un diccionario (desde base de datos)
        return cls(
            id=data.get('id'),
            proveedor=data['proveedor'],
            cliente=data['cliente'],
            destino=data['destino'],
            estado=data['estado'],
            numero_seguimiento=data['numero_seguimiento'],
            fecha_entrega=data['fecha_entrega'],
            fecha_ingreso=data.get('fecha_ingreso')  # Usa la fecha de la BD
        )