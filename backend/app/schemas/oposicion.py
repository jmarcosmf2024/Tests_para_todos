"""
Esquemas Pydantic para oposiciones, cuerpos, regiones y preferencias de usuario.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RegionResponse(BaseModel):
    """Schema para respuesta de región."""
    id: int = Field(..., description="ID de la región")
    nombre: str = Field(..., description="Nombre de la región")
    codigo: str = Field(..., description="Código de la región")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Comunidad de Madrid",
                "codigo": "MAD"
            }
        }


class CuerpoResponse(BaseModel):
    """Schema para respuesta de cuerpo de oposición."""
    id: int = Field(..., description="ID del cuerpo")
    nombre: str = Field(..., description="Nombre del cuerpo")
    descripcion: Optional[str] = Field(None, description="Descripción del cuerpo")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Policía Nacional",
                "descripcion": "Cuerpo de Policía Nacional"
            }
        }


class OposicionResponse(BaseModel):
    """Schema para respuesta de oposición."""
    id: int = Field(..., description="ID de la oposición")
    nombre: str = Field(..., description="Nombre de la oposición")
    descripcion: Optional[str] = Field(None, description="Descripción de la oposición")
    cuerpo_id: int = Field(..., description="ID del cuerpo relacionado")
    activa: bool = Field(..., description="Si la oposición está activa")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Policía Nacional 2024",
                "descripcion": "Oposición a Policía Nacional convocatoria 2024",
                "cuerpo_id": 1,
                "activa": True
            }
        }


class TemaResponse(BaseModel):
    """Schema para respuesta de tema."""
    id: int = Field(..., description="ID del tema")
    numero: int = Field(..., description="Número del tema")
    titulo: str = Field(..., description="Título del tema")
    oposicion_id: int = Field(..., description="ID de la oposición")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "numero": 1,
                "titulo": "Constitución Española",
                "oposicion_id": 1
            }
        }


class PreferenciaUsuarioBase(BaseModel):
    """Schema base para preferencias de usuario."""
    oposicion_id: Optional[int] = Field(None, description="ID de la oposición seleccionada")
    cuerpo_id: Optional[int] = Field(None, description="ID del cuerpo seleccionado")
    region_id: Optional[int] = Field(None, description="ID de la región seleccionada")
    
    class Config:
        schema_extra = {
            "example": {
                "oposicion_id": 1,
                "cuerpo_id": 1,
                "region_id": 1
            }
        }


class PreferenciaUsuarioCreate(PreferenciaUsuarioBase):
    """Schema para crear/actualizar preferencias de usuario."""
    pass


class PreferenciaUsuarioResponse(PreferenciaUsuarioBase):
    """Schema para respuesta de preferencias de usuario."""
    id: int = Field(..., description="ID de la preferencia")
    usuario_id: int = Field(..., description="ID del usuario")
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    
    class Config:
        from_attributes = True


class ListaOposicionesResponse(BaseModel):
    """Schema para respuesta de lista de oposiciones."""
    id: int
    nombre: str
    descripcion: Optional[str]
    cuerpo_id: int
    activa: bool
    
    class Config:
        from_attributes = True


class ListaCuerposResponse(BaseModel):
    """Schema para respuesta de lista de cuerpos."""
    id: int
    nombre: str
    descripcion: Optional[str]
    
    class Config:
        from_attributes = True


class ListaRegionesResponse(BaseModel):
    """Schema para respuesta de lista de regiones."""
    id: int
    nombre: str
    codigo: str
    
    class Config:
        from_attributes = True


class ListaTemasResponse(BaseModel):
    """Schema para respuesta de lista de temas."""
    id: int
    numero: int
    titulo: str
    oposicion_id: int
    
    class Config:
        from_attributes = True
