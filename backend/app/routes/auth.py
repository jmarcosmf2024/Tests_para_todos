"""
Rutas de autenticación: registro, login, refresh token, etc.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import Usuario
from app.schemas.user import (
    UsuarioRegistro,
    UsuarioLogin,
    TokenResponse,
    UsuarioResponse,
    CambiarContraseña,
    RefreshTokenRequest,
    MensajeResponse
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_active_user
)
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["autenticación"])


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario"
)
def registrar_usuario(usuario_data: UsuarioRegistro, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en la plataforma.
    
    **Parámetros:**
    - **email**: Correo electrónico único
    - **nombre**: Nombre del usuario
    - **apellidos**: Apellidos del usuario
    - **contraseña**: Contraseña (mínimo 8 caracteres)
    
    **Retorna:** Datos del usuario creado
    """
    
    # Verificar si el email ya existe
    usuario_existente = db.query(Usuario).filter(
        Usuario.email == usuario_data.email
    ).first()
    
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado"
        )
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        email=usuario_data.email,
        nombre=usuario_data.nombre,
        apellidos=usuario_data.apellidos,
        contraseña_hash=hash_password(usuario_data.contraseña),
        activo=True
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve tokens JWT"
)
def login(credenciales: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Autentica un usuario y devuelve tokens de acceso y refresco.
    
    **Parámetros:**
    - **email**: Correo electrónico del usuario
    - **contraseña**: Contraseña del usuario
    
    **Retorna:** Tokens JWT (acceso y refresco)
    """
    
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == credenciales.email).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar contraseña
    if not verify_password(credenciales.contraseña, usuario.contraseña_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que el usuario está activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear tokens
    access_token = create_access_token(data={"sub": str(usuario.id)})
    refresh_token = create_refresh_token(data={"sub": str(usuario.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refrescar token de acceso",
    description="Genera un nuevo token de acceso usando el refresh token"
)
def refrescar_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Genera un nuevo token de acceso usando el refresh token.
    
    **Parámetros:**
    - **refresh_token**: Token de refresco válido
    
    **Retorna:** Nuevo token de acceso
    """
    
    # Verificar el refresh token
    payload = verify_token(request.refresh_token)
    
    usuario_id: int = int(payload.get("sub"))
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear nuevo access token
    access_token = create_access_token(data={"sub": str(usuario.id)})
    refresh_token = create_refresh_token(data={"sub": str(usuario.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener datos del usuario actual",
    description="Devuelve los datos del usuario autenticado"
)
def obtener_usuario_actual(
    usuario_actual: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene los datos del usuario actualmente autenticado.
    
    **Retorna:** Datos del usuario actual
    """
    return usuario_actual


@router.put(
    "/cambiar-contraseña",
    response_model=MensajeResponse,
    status_code=status.HTTP_200_OK,
    summary="Cambiar contraseña",
    description="Cambia la contraseña del usuario autenticado"
)
def cambiar_contraseña(
    datos: CambiarContraseña,
    usuario_actual: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cambia la contraseña del usuario autenticado.
    
    **Parámetros:**
    - **contraseña_actual**: Contraseña actual del usuario
    - **contraseña_nueva**: Nueva contraseña (mínimo 8 caracteres)
    - **contraseña_confirmacion**: Confirmación de la nueva contraseña
    
    **Retorna:** Mensaje de confirmación
    """
    
    # Verificar que la contraseña actual es correcta
    if not verify_password(datos.contraseña_actual, usuario_actual.contraseña_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña actual incorrecta"
        )
    
    # Verificar que las contraseñas nuevas coinciden
    if datos.contraseña_nueva != datos.contraseña_confirmacion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las nuevas contraseñas no coinciden"
        )
    
    # Verificar que la nueva contraseña es diferente a la actual
    if verify_password(datos.contraseña_nueva, usuario_actual.contraseña_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe ser diferente a la actual"
        )
    
    # Actualizar contraseña
    usuario_actual.contraseña_hash = hash_password(datos.contraseña_nueva)
    db.add(usuario_actual)
    db.commit()
    
    return {"mensaje": "Contraseña actualizada correctamente"}


@router.post(
    "/logout",
    response_model=MensajeResponse,
    status_code=status.HTTP_200_OK,
    summary="Cerrar sesión",
    description="Cierra la sesión del usuario autenticado"
)
def logout(usuario_actual: Usuario = Depends(get_current_active_user)):
    """
    Cierra la sesión del usuario.
    
    Nota: En una arquitectura JWT, el logout se realiza en el cliente
    eliminando los tokens. Este endpoint puede ser usado para registro
    de auditoría si es necesario.
    
    **Retorna:** Mensaje de confirmación
    """
    return {"mensaje": "Sesión cerrada correctamente"}
