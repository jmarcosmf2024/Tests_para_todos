"""
Rutas para gestión de oposiciones, cuerpos, regiones y preferencias de usuario.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import Usuario
from app.models.oposicion import Oposicion, Cuerpo, Region, Tema, PreferenciaUsuario
from app.schemas.oposicion import (
    OposicionResponse,
    CuerpoResponse,
    RegionResponse,
    TemaResponse,
    PreferenciaUsuarioCreate,
    PreferenciaUsuarioResponse,
    ListaOposicionesResponse,
    ListaCuerposResponse,
    ListaRegionesResponse,
    ListaTemasResponse
)
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/api", tags=["oposiciones"])


# ==================== ENDPOINTS DE OPOSICIONES ====================

@router.get(
    "/oposiciones",
    response_model=list[ListaOposicionesResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las oposiciones",
    description="Obtiene la lista de todas las oposiciones disponibles"
)
def listar_oposiciones(
    activas_solo: bool = True,
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de oposiciones disponibles.
    
    **Parámetros:**
    - **activas_solo**: Si es True, solo devuelve oposiciones activas (default: True)
    
    **Retorna:** Lista de oposiciones
    """
    query = db.query(Oposicion)
    
    if activas_solo:
        query = query.filter(Oposicion.activa == True)
    
    oposiciones = query.all()
    return oposiciones


@router.get(
    "/oposiciones/{oposicion_id}",
    response_model=OposicionResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener oposición por ID",
    description="Obtiene los detalles de una oposición específica"
)
def obtener_oposicion(
    oposicion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de una oposición específica.
    
    **Parámetros:**
    - **oposicion_id**: ID de la oposición
    
    **Retorna:** Datos de la oposición
    """
    oposicion = db.query(Oposicion).filter(Oposicion.id == oposicion_id).first()
    
    if not oposicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oposición no encontrada"
        )
    
    return oposicion


# ==================== ENDPOINTS DE CUERPOS ====================

@router.get(
    "/cuerpos",
    response_model=list[ListaCuerposResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los cuerpos",
    description="Obtiene la lista de todos los cuerpos disponibles"
)
def listar_cuerpos(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los cuerpos de oposición.
    
    **Retorna:** Lista de cuerpos
    """
    cuerpos = db.query(Cuerpo).all()
    return cuerpos


@router.get(
    "/cuerpos/{cuerpo_id}",
    response_model=CuerpoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener cuerpo por ID",
    description="Obtiene los detalles de un cuerpo específico"
)
def obtener_cuerpo(
    cuerpo_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de un cuerpo específico.
    
    **Parámetros:**
    - **cuerpo_id**: ID del cuerpo
    
    **Retorna:** Datos del cuerpo
    """
    cuerpo = db.query(Cuerpo).filter(Cuerpo.id == cuerpo_id).first()
    
    if not cuerpo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuerpo no encontrado"
        )
    
    return cuerpo


# ==================== ENDPOINTS DE REGIONES ====================

@router.get(
    "/regiones",
    response_model=list[ListaRegionesResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las regiones",
    description="Obtiene la lista de todas las regiones disponibles"
)
def listar_regiones(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todas las regiones.
    
    **Retorna:** Lista de regiones
    """
    regiones = db.query(Region).all()
    return regiones


@router.get(
    "/regiones/{region_id}",
    response_model=RegionResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener región por ID",
    description="Obtiene los detalles de una región específica"
)
def obtener_region(
    region_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de una región específica.
    
    **Parámetros:**
    - **region_id**: ID de la región
    
    **Retorna:** Datos de la región
    """
    region = db.query(Region).filter(Region.id == region_id).first()
    
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Región no encontrada"
        )
    
    return region


# ==================== ENDPOINTS DE TEMAS ====================

@router.get(
    "/oposiciones/{oposicion_id}/temas",
    response_model=list[ListaTemasResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar temas de una oposición",
    description="Obtiene la lista de temas de una oposición específica"
)
def listar_temas_oposicion(
    oposicion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de temas de una oposición.
    
    **Parámetros:**
    - **oposicion_id**: ID de la oposición
    
    **Retorna:** Lista de temas
    """
    # Verificar que la oposición existe
    oposicion = db.query(Oposicion).filter(Oposicion.id == oposicion_id).first()
    if not oposicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oposición no encontrada"
        )
    
    temas = db.query(Tema).filter(Tema.oposicion_id == oposicion_id).order_by(Tema.numero).all()
    return temas


@router.get(
    "/temas/{tema_id}",
    response_model=TemaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener tema por ID",
    description="Obtiene los detalles de un tema específico"
)
def obtener_tema(
    tema_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de un tema específico.
    
    **Parámetros:**
    - **tema_id**: ID del tema
    
    **Retorna:** Datos del tema
    """
    tema = db.query(Tema).filter(Tema.id == tema_id).first()
    
    if not tema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tema no encontrado"
        )
    
    return tema


# ==================== ENDPOINTS DE PREFERENCIAS ====================

@router.get(
    "/preferencias",
    response_model=PreferenciaUsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener preferencias del usuario actual",
    description="Obtiene las preferencias de oposición, cuerpo y región del usuario autenticado"
)
def obtener_preferencias(
    usuario_actual: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene las preferencias de oposición, cuerpo y región del usuario actual.
    
    **Retorna:** Preferencias del usuario
    """
    preferencias = db.query(PreferenciaUsuario).filter(
        PreferenciaUsuario.usuario_id == usuario_actual.id
    ).first()
    
    if not preferencias:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferencias no encontradas"
        )
    
    return preferencias


@router.post(
    "/preferencias",
    response_model=PreferenciaUsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear preferencias de usuario",
    description="Crea las preferencias de oposición, cuerpo y región para el usuario autenticado"
)
def crear_preferencias(
    datos: PreferenciaUsuarioCreate,
    usuario_actual: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crea las preferencias de oposición, cuerpo y región del usuario.
    
    **Parámetros:**
    - **oposicion_id**: ID de la oposición seleccionada (opcional)
    - **cuerpo_id**: ID del cuerpo seleccionado (opcional)
    - **region_id**: ID de la región seleccionada (opcional)
    
    **Retorna:** Preferencias creadas
    """
    # Verificar que no existan preferencias previas
    preferencias_existentes = db.query(PreferenciaUsuario).filter(
        PreferenciaUsuario.usuario_id == usuario_actual.id
    ).first()
    
    if preferencias_existentes:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya tiene preferencias registradas"
        )
    
    # Validar que los IDs existen (si se proporcionan)
    if datos.oposicion_id:
        oposicion = db.query(Oposicion).filter(Oposicion.id == datos.oposicion_id).first()
        if not oposicion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Oposición no encontrada"
            )
    
    if datos.cuerpo_id:
        cuerpo = db.query(Cuerpo).filter(Cuerpo.id == datos.cuerpo_id).first()
        if not cuerpo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cuerpo no encontrado"
            )
    
    if datos.region_id:
        region = db.query(Region).filter(Region.id == datos.region_id).first()
        if not region:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Región no encontrada"
            )
    
    # Crear preferencias
    preferencias = PreferenciaUsuario(
        usuario_id=usuario_actual.id,
        oposicion_id=datos.oposicion_id,
        cuerpo_id=datos.cuerpo_id,
        region_id=datos.region_id
    )
    
    db.add(preferencias)
    db.commit()
    db.refresh(preferencias)
    
    return preferencias


@router.put(
    "/preferencias",
    response_model=PreferenciaUsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar preferencias de usuario",
    description="Actualiza las preferencias de oposición, cuerpo y región del usuario autenticado"
)
def actualizar_preferencias(
    datos: PreferenciaUsuarioCreate,
    usuario_actual: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza las preferencias de oposición, cuerpo y región del usuario.
    
    **Parámetros:**
    - **oposicion_id**: ID de la oposición seleccionada (opcional)
    - **cuerpo_id**: ID del cuerpo seleccionado (opcional)
    - **region_id**: ID de la región seleccionada (opcional)
    
    **Retorna:** Preferencias actualizadas
    """
    preferencias = db.query(PreferenciaUsuario).filter(
        PreferenciaUsuario.usuario_id == usuario_actual.id
    ).first()
    
    if not preferencias:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferencias no encontradas"
        )
    
    # Validar que los IDs existen (si se proporcionan)
    if datos.oposicion_id:
        oposicion = db.query(Oposicion).filter(Oposicion.id == datos.oposicion_id).first()
        if not oposicion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Oposición no encontrada"
            )
    
    if datos.cuerpo_id:
        cuerpo = db.query(Cuerpo).filter(Cuerpo.id == datos.cuerpo_id).first()
        if not cuerpo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cuerpo no encontrado"
            )
    
    if datos.region_id:
        region = db.query(Region).filter(Region.id == datos.region_id).first()
        if not region:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Región no encontrada"
            )
    
    # Actualizar preferencias
    preferencias.oposicion_id = datos.oposicion_id
    preferencias.cuerpo_id = datos.cuerpo_id
    preferencias.region_id = datos.region_id
    
    db.add(preferencias)
    db.commit()
    db.refresh(preferencias)
    
    return preferencias
