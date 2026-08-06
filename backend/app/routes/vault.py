from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.models.user import User, Secret
from backend.app.models.schemas import SecretCreate, SecretUpdate, SecretResponse, SecretDetailResponse
from backend.app.services.auth import get_current_user
from backend.app.services.crypto import encrypt_value, decrypt_value

router = APIRouter(prefix="/api/vault", tags=["Secrets Vault"])


@router.post("/secrets", response_model=SecretResponse, status_code=status.HTTP_201_CREATED)
async def create_secret(
    data: SecretCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    secret = Secret(
        owner_id=current_user.id,
        title=data.title,
        encrypted_value=encrypt_value(data.value),
    )
    db.add(secret)
    await db.commit()
    await db.refresh(secret)
    return secret


@router.get("/secrets", response_model=list[SecretResponse])
async def list_secrets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Secret).where(Secret.owner_id == current_user.id))
    return result.scalars().all()


@router.get("/secrets/{secret_id}", response_model=SecretDetailResponse)
async def get_secret(
    secret_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Secret).where(Secret.id == secret_id, Secret.owner_id == current_user.id)
    )
    secret = result.scalar_one_or_none()
    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    return SecretDetailResponse(
        id=secret.id,
        title=secret.title,
        value=decrypt_value(secret.encrypted_value),
        created_at=secret.created_at,
        updated_at=secret.updated_at,
    )


@router.put("/secrets/{secret_id}", response_model=SecretResponse)
async def update_secret(
    secret_id: str,
    data: SecretUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Secret).where(Secret.id == secret_id, Secret.owner_id == current_user.id)
    )
    secret = result.scalar_one_or_none()
    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    if data.title is not None:
        secret.title = data.title
    if data.value is not None:
        secret.encrypted_value = encrypt_value(data.value)

    await db.commit()
    await db.refresh(secret)
    return secret


@router.delete("/secrets/{secret_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_secret(
    secret_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Secret).where(Secret.id == secret_id, Secret.owner_id == current_user.id)
    )
    secret = result.scalar_one_or_none()
    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    await db.delete(secret)
    await db.commit()
