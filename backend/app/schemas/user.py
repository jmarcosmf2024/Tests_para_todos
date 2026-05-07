"""
Esquemas Pydantic para validación de datos de usuarios.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioRegistro(BaseModel):
    """Schema para registro de nuevo usuario."""
    email: EmailStr = Field(..., description="Correo electrónico único")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    apellidos: str = Field(..., min_length=2, max_length=100, description="Apellidos del usuario")
    contraseña: str = Field(..., min_length=8, max_length=100, description="Contraseña (mínimo 8 caracteres)")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "nombre": "Juan",
                "apellidos": "García López",
                "contraseña": "MiContraseña123!"
            }
        }


class UsuarioLogin(BaseModel):
    """Schema para login de usuario."""
    email: EmailStr = Field(..., description="Correo electrónico")
    contraseña: str = Field(..., description="Contraseña")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "contraseña": "MiContraseña123!"
            }
        }


class TokenResponse(BaseModel):
    """Schema para respuesta de token de autenticación."""
    access_token: str = Field(..., description="Token JWT de acceso")
    refresh_token: str = Field(..., description="Token JWT de refresco")
    token_type: str = Field(default="bearer", description="Tipo de token")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class UsuarioResponse(BaseModel):
    """Schema para respuesta de datos de usuario."""
    id: int = Field(..., description="ID del usuario")
    email: str = Field(..., description="Correo electrónico")
    nombre: str = Field(..., description="Nombre del usuario")
    apellidos: str = Field(..., description="Apellidos del usuario")
    activo: bool = Field(..., description="Si el usuario está activo")
    fecha_registro: datetime = Field(..., description="Fecha de registro")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "email": "usuario@example.com",
                "nombre": "Juan",
                "apellidos": "García López",
                "activo": True,
                "fecha_registro": "2026-05-07T10:06:34"
            }
        }


class CambiarContraseña(BaseModel):
    """Schema para cambiar contraseña."""
    contraseña_actual: str = Field(..., description="Contraseña actual")
    contraseña_nueva: str = Field(..., min_length=8, max_length=100, description="Nueva contraseña")
    contraseña_confirmacion: str = Field(..., description="Confirmación de nueva contraseña")
    
    class Config:
        schema_extra = {
            "example": {
                "contraseña_actual": "ContraseñaAntigua123!",
                "contraseña_nueva": "ContraseñaNueva456!",
                "contraseña_confirmacion": "ContraseñaNueva456!"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Schema para solicitud de refresco de token."""
    refresh_token: str = Field(..., description="Token de refresco")
    
    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class MensajeResponse(BaseModel):
    """Schema genérico para respuestas de mensaje."""
    mensaje: str = Field(..., description="Mensaje de respuesta")
    
    class Config:
        schema_extra = {
            "example": {
                "mensaje": "Operación realizada exitosamente"
            }
        }
