"""
Esquemas Pydantic para preguntas, tests y respuestas de usuario.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TipoPreguntaEnum(str, Enum):
    """Tipos de preguntas disponibles."""
    MULTIPLE_CHOICE = "multiple_choice"
    VERDADERO_FALSO = "verdadero_falso"
    RESPUESTA_CORTA = "respuesta_corta"


class OpcionResponse(BaseModel):
    """Schema para opción de pregunta múltiple."""
    id: int = Field(..., description="ID de la opción")
    texto: str = Field(..., description="Texto de la opción")
    es_correcta: Optional[bool] = Field(None, description="Si es la opción correcta (solo para respuesta)")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "texto": "Madrid",
                "es_correcta": True
            }
        }


class PreguntaResponse(BaseModel):
    """Schema para respuesta de pregunta."""
    id: int = Field(..., description="ID de la pregunta")
    numero: int = Field(..., description="Número de la pregunta en el test")
    tema_id: int = Field(..., description="ID del tema")
    tipo: TipoPreguntaEnum = Field(..., description="Tipo de pregunta")
    texto: str = Field(..., description="Texto de la pregunta")
    opciones: Optional[List[OpcionResponse]] = Field(None, description="Opciones disponibles (si aplica)")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "numero": 1,
                "tema_id": 1,
                "tipo": "multiple_choice",
                "texto": "¿Cuál es la capital de España?",
                "opciones": [
                    {"id": 1, "texto": "Madrid"},
                    {"id": 2, "texto": "Barcelona"},
                    {"id": 3, "texto": "Valencia"}
                ]
            }
        }


class TestResponse(BaseModel):
    """Schema para respuesta de test."""
    id: int = Field(..., description="ID del test")
    nombre: str = Field(..., description="Nombre del test")
    descripcion: Optional[str] = Field(None, description="Descripción del test")
    tema_id: int = Field(..., description="ID del tema")
    año: int = Field(..., description="Año del test")
    numero_preguntas: int = Field(..., description="Número de preguntas")
    activo: bool = Field(..., description="Si el test está activo")
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Test Tema 1 - 2024",
                "descripcion": "Test de práctica del tema 1",
                "tema_id": 1,
                "año": 2024,
                "numero_preguntas": 25,
                "activo": True,
                "fecha_creacion": "2026-05-07T10:00:00"
            }
        }


class TestDetalladoResponse(TestResponse):
    """Schema para respuesta detallada de test con preguntas."""
    preguntas: List[PreguntaResponse] = Field(..., description="Lista de preguntas del test")
    
    class Config:
        from_attributes = True


class RespuestaUsuarioCreate(BaseModel):
    """Schema para crear respuesta de usuario a una pregunta."""
    pregunta_id: int = Field(..., description="ID de la pregunta")
    opcion_id: Optional[int] = Field(None, description="ID de la opción seleccionada (si aplica)")
    texto_respuesta: Optional[str] = Field(None, description="Texto de la respuesta (si aplica)")
    
    class Config:
        schema_extra = {
            "example": {
                "pregunta_id": 1,
                "opcion_id": 1,
                "texto_respuesta": None
            }
        }


class RespuestaUsuarioResponse(RespuestaUsuarioCreate):
    """Schema para respuesta de usuario completada."""
    id: int = Field(..., description="ID de la respuesta")
    usuario_id: int = Field(..., description="ID del usuario")
    es_correcta: Optional[bool] = Field(None, description="Si la respuesta es correcta")
    fecha_respuesta: datetime = Field(..., description="Fecha de la respuesta")
    
    class Config:
        from_attributes = True


class IntentoPrueba(BaseModel):
    """Schema para un intento de prueba de test."""
    id: int = Field(..., description="ID del intento")
    usuario_id: int = Field(..., description="ID del usuario")
    test_id: int = Field(..., description="ID del test")
    fecha_inicio: datetime = Field(..., description="Fecha de inicio")
    fecha_finalizacion: Optional[datetime] = Field(None, description="Fecha de finalización")
    puntuacion: Optional[float] = Field(None, description="Puntuación obtenida (0-100)")
    correctas: Optional[int] = Field(None, description="Número de respuestas correctas")
    incorrectas: Optional[int] = Field(None, description="Número de respuestas incorrectas")
    sin_responder: Optional[int] = Field(None, description="Número de preguntas sin responder")
    estado: str = Field(..., description="Estado del intento (en_progreso, finalizado)")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "usuario_id": 1,
                "test_id": 1,
                "fecha_inicio": "2026-05-07T10:00:00",
                "fecha_finalizacion": "2026-05-07T11:00:00",
                "puntuacion": 85.5,
                "correctas": 21,
                "incorrectas": 3,
                "sin_responder": 1,
                "estado": "finalizado"
            }
        }


class IntentoDetalladoResponse(IntentoPrueba):
    """Schema para respuesta detallada del intento con respuestas."""
    respuestas: List[RespuestaUsuarioResponse] = Field(..., description="Respuestas del usuario")
    
    class Config:
        from_attributes = True


class EstadisticasUsuarioResponse(BaseModel):
    """Schema para estadísticas de usuario."""
    total_intentos: int = Field(..., description="Total de intentos realizados")
    tests_completados: int = Field(..., description="Tests completados")
    puntuacion_promedio: float = Field(..., description="Puntuación promedio")
    total_preguntas_respondidas: int = Field(..., description="Total de preguntas respondidas")
    total_respuestas_correctas: int = Field(..., description="Total de respuestas correctas")
    porcentaje_acierto: float = Field(..., description="Porcentaje de acierto")
    
    class Config:
        schema_extra = {
            "example": {
                "total_intentos": 10,
                "tests_completados": 10,
                "puntuacion_promedio": 78.5,
                "total_preguntas_respondidas": 250,
                "total_respuestas_correctas": 195,
                "porcentaje_acierto": 78.0
            }
        }


class ListaTestsResponse(BaseModel):
    """Schema para respuesta de lista de tests."""
    id: int
    nombre: str
    descripcion: Optional[str]
    tema_id: int
    año: int
    numero_preguntas: int
    activo: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True


class ListaIntentosResponse(BaseModel):
    """Schema para respuesta de lista de intentos."""
    id: int
    usuario_id: int
    test_id: int
    fecha_inicio: datetime
    fecha_finalizacion: Optional[datetime]
    puntuacion: Optional[float]
    correctas: Optional[int]
    incorrectas: Optional[int]
    sin_responder: Optional[int]
    estado: str
    
    class Config:
        from_attributes = True
