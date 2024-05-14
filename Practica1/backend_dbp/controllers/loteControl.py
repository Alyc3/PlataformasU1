from models.producto import Producto
from models.lote import Lote
from controllers.utils.errors import Erros
import uuid
from app import db
import jwt
from datetime import datetime, timedelta
from flask import current_app

class LoteControl:

    # Metodo para listar lotes
    def listar(self):
        return Lote.query.all()
    
    # Metodo para guardar lote
    def guardar(self, data):
        lote = Lote()
        lote.nombrePr = data.get('nombrePr')  
        fechaPr = data.get('fechaPr')
        if fechaPr:
           lote.fechaPr = datetime.strptime(fechaPr, '%d/%m/%Y').strftime('%Y-%m-%d')
        fechaVen = data.get('fechaVen')
        if fechaVen:
           lote.fechaVen = datetime.strptime(fechaVen, '%d/%m/%Y').strftime('%Y-%m-%d')
        lote.cantidadL = data.get('cantidadL')
        lote.estadoPr = 'Buen_Estado'
        lote.external_id = uuid.uuid4()
        db.session.add(lote)
        db.session.commit()
        return lote.id
    
    def listar_PorCaducar(self):
        hoy = datetime.now().date()
        lotes = Lote.query.all()
        lotes_por_caducar = []
        for lote in lotes:
            if lote.fechaVen is not None:
                if lote.fechaVen - timedelta(days=5) <= hoy < lote.fechaVen:
                    lote.estadoPr = 'PorCaducar'
                    lotes_por_caducar.append(lote)
                elif lote.fechaVen == hoy:
                    lote.estadoPr = 'Vencido'
                    lotes_por_caducar.append(lote)
            db.session.commit()
        return lotes_por_caducar
    
    def listar_vencidos(self):
        # Obtén la fecha actual
        hoy = datetime.now().date()
        # Obtén todos los lotes
        lotes = Lote.query.all()
        lotes_vencidos = []
        for lote in lotes:
            productos_del_lote = Producto.query.filter_by(id_lote=lote.id).all()
            # Verifica si el lote está vencido o por vencer
            if lote.fechaVen < hoy or lote.estadoPr == "Vencido":
                lote.estadoPr = "Vencido"
                # Actualiza el stock de todos los productos en el lote a 0
                for producto in productos_del_lote:
                    producto.stock = 0
                print(f"Lote actualizado: {lote.nombrePr}, Estado: {lote.estadoPr}")
                lotes_vencidos.append(lote.serialize)
    
        db.session.commit()
    
        return lotes_vencidos
    
    def listar_LVencido(self):
       return Lote.query.filter_by(estadoPr='Vencido').all()

    
    
