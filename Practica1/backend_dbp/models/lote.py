from app import db
from models.estadoPr import EstadoPr
import uuid

class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    nombrePr = db.Column(db.String(100))
    fechaPr = db.Column(db.Date)
    fechaVen=db.Column(db.Date)
    cantidadL = db.Column(db.Integer)
    estadoPr = db.Column(db.Enum(EstadoPr), nullable = False,default='Buen_Estado')
    # Relación uno a muchos con Producto
    producto = db.relationship('Producto', back_populates='lote', lazy=True)
    
    
    @property
    def serialize(self):
        return {
            'nombrePr': self.nombrePr,
            'fechaPr': self.fechaPr.isoformat() if self.fechaPr else None,
            'fechaVen': self.fechaVen.isoformat() if self.fechaVen else None,
            'cantidadL': self.cantidadL,
            'estadoPr': self.estadoPr.value
        }
        
    
    def copy(self):
        new_lote = Lote(
            id=self.id,
            nombrePr=self.nombrePr,
            fechaPr=self.fechaPr,
            fechaVen=self.fechaVen,
            cantidadL=self.cantidadL,
            estadoPr=self.estadoPr
        )