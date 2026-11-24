import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased

from app.auth import get_usuario_atual
from app.database import get_db

from app.models.campanha import Campanha
from app.models.campanha_usuario import CampanhaUsuario
from app.models.combate import Combate
from app.models.combate_participante import CombateParticipante
from app.models.criatura import Criatura
from app.models.personagem import Personagem
from app.models.usuario import Usuario

from app.schemas.campanha_schema import (
    CampanhaCreate,
    CampanhaEntrar,
    CampanhaParticipanteResponse,
    CampanhaResponse,
    CampanhaUpdate,
)

from app.schemas.combate_schema import (
    CombateCreate,
    CombateCriaturaAdicionar,
    CombateParticipanteListResponse,
    CombateParticipanteResponse,
    CombateParticipanteUpdate,
    CombatePersonagemAdicionar,
    CombateResponse,
)

def gerar_codigo_convite() -> str:
    return secrets.token_hex(6).upper()

def obter_nome_mestre(campanha_id: int, db: Session) -> str:
    consulta = (
        select(Usuario.nome)
        .join(
            CampanhaUsuario,
            CampanhaUsuario.usuario_id == Usuario.id,
        )
        .where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.papel == "MESTRE",
        )
    )

    nome_mestre = db.scalar(consulta)

    return nome_mestre

def buscar_combate_do_mestre(
    campanha_id: int,
    combate_id: int,
    usuario: Usuario,
    db: Session,
) -> Combate:
    associacao = db.scalar(
        select(CampanhaUsuario).where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    if associacao.papel != "MESTRE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o Mestre pode gerenciar o combate.",
        )

    combate = db.scalar(
        select(Combate).where(
            Combate.id == combate_id,
            Combate.campanha_id == campanha_id,
        )
    )

    if combate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combate não encontrado.",
        )

    if combate.status != "ATIVO":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível alterar um combate encerrado.",
        )

    return combate

router = APIRouter(
    prefix="/campanhas",
    tags=["Campanhas"],
)


@router.post(
    "/",
    response_model=CampanhaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_campanha(
    dados: CampanhaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    for tentativa in range(5):
        campanha = Campanha(
            nome=dados.nome,
            descricao=dados.descricao,
            codigo_convite=gerar_codigo_convite(),
        )

        try:
            db.add(campanha)
            db.flush()

            associacao = CampanhaUsuario(
                campanha_id=campanha.id,
                usuario_id=usuario.id,
                papel="MESTRE",
            )

            db.add(associacao)
            db.commit()
            db.refresh(campanha)

            return CampanhaResponse(
                id=campanha.id,
                nome=campanha.nome,
                nome_mestre=usuario.nome,
                descricao=campanha.descricao,
                data_criacao=campanha.data_criacao,
                codigo_convite=campanha.codigo_convite,
)

        except IntegrityError:
            db.rollback()

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Não foi possível gerar um código de convite exclusivo.",
    )


@router.get(
    "/",
    response_model=list[CampanhaResponse],
)
def listar_campanhas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    AssociacaoMestre = aliased(CampanhaUsuario)

    consulta = (
        select(
            Campanha,
            Usuario.nome.label("nome_mestre"),
        )
        # Filtra campanhas das quais o usuário atual participa.
        .join(
            CampanhaUsuario,
            CampanhaUsuario.campanha_id == Campanha.id,
        )
        # Encontra a associação do Mestre da campanha.
        .join(
            AssociacaoMestre,
            (AssociacaoMestre.campanha_id == Campanha.id)
            & (AssociacaoMestre.papel == "MESTRE"),
        )
        # Busca o nome do usuário que é o Mestre.
        .join(
            Usuario,
            Usuario.id == AssociacaoMestre.usuario_id,
        )
        .where(
            CampanhaUsuario.usuario_id == usuario.id,
        )
        .order_by(Campanha.data_criacao.desc())
    )

    resultados = db.execute(consulta).all()

    return [
        CampanhaResponse(
            id=campanha.id,
            nome=campanha.nome,
            nome_mestre=nome_mestre,
            descricao=campanha.descricao,
            data_criacao=campanha.data_criacao,
            codigo_convite=campanha.codigo_convite,
        )
        for campanha, nome_mestre in resultados
    ]

@router.put(
    "/{campanha_id}",
    response_model=CampanhaResponse,
)
def atualizar_campanha(
    campanha_id: int,
    dados: CampanhaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    consulta = (
        select(CampanhaUsuario)
        .where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    associacao = db.scalar(consulta)

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    if associacao.papel != "MESTRE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o Mestre pode editar a campanha.",
        )

    campanha = db.get(Campanha, campanha_id)

    campanha.nome = dados.nome
    campanha.descricao = dados.descricao

    db.commit()
    db.refresh(campanha)

    return CampanhaResponse(
        id=campanha.id,
        nome=campanha.nome,
        nome_mestre=obter_nome_mestre(campanha.id, db),
        descricao=campanha.descricao,
        data_criacao=campanha.data_criacao,
        codigo_convite=campanha.codigo_convite,
)



@router.delete(
    "/{campanha_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_campanha(
    campanha_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    consulta = (
        select(CampanhaUsuario)
        .where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    associacao = db.scalar(consulta)

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    if associacao.papel != "MESTRE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o Mestre pode excluir a campanha.",
        )

    campanha = db.get(Campanha, campanha_id)

    db.delete(campanha)
    db.commit()

@router.post(
    "/entrar",
    response_model=CampanhaResponse,
)
def entrar_em_campanha(
    dados: CampanhaEntrar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    campanha = db.scalar(
        select(Campanha).where(
            Campanha.codigo_convite == dados.codigo_convite.strip().upper()
        )
    )

    if campanha is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de convite inválido.",
        )

    associacao_existente = db.scalar(
        select(CampanhaUsuario).where(
            CampanhaUsuario.campanha_id == campanha.id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    if associacao_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já participa desta campanha.",
        )

    personagem = db.scalar(
        select(Personagem).where(
            Personagem.id == dados.personagem_id,
            Personagem.usuario_id == usuario.id,
        )
    )

    if personagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado.",
        )

    associacao = CampanhaUsuario(
        campanha_id=campanha.id,
        usuario_id=usuario.id,
        papel="JOGADOR",
        personagem_id=personagem.id,
    )

    try:
        db.add(associacao)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível entrar na campanha.",
        )

    return CampanhaResponse(
        id=campanha.id,
        nome=campanha.nome,
        nome_mestre=obter_nome_mestre(campanha.id, db),
        descricao=campanha.descricao,
        data_criacao=campanha.data_criacao,
        codigo_convite=campanha.codigo_convite,
)

@router.get(
    "/{campanha_id}/participantes",
    response_model=list[CampanhaParticipanteResponse],
)
def listar_participantes(
    campanha_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    associacao = db.scalar(
        select(CampanhaUsuario).where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    consulta = (
        select(
            Usuario.id.label("usuario_id"),
            Usuario.nome.label("nome_usuario"),
            CampanhaUsuario.papel,
            Personagem.id.label("personagem_id"),
            Personagem.nome.label("nome_personagem"),
        )
        .join(
            CampanhaUsuario,
            CampanhaUsuario.usuario_id == Usuario.id,
        )
        .outerjoin(
            Personagem,
            Personagem.id == CampanhaUsuario.personagem_id,
        )
        .where(
            CampanhaUsuario.campanha_id == campanha_id,
        )
        .order_by(CampanhaUsuario.papel, Usuario.nome)
    )

    participantes = db.execute(consulta).all()

    return [
        CampanhaParticipanteResponse(
            usuario_id=participante.usuario_id,
            nome_usuario=participante.nome_usuario,
            papel=participante.papel,
            personagem_id=participante.personagem_id,
            nome_personagem=participante.nome_personagem,
        )
        for participante in participantes
    ]


@router.post(
    "/{campanha_id}/combates",
    response_model=CombateResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_combate(
    campanha_id: int,
    dados: CombateCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):

    associacao = db.scalar(
        select(CampanhaUsuario).where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    if associacao.papel != "MESTRE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o Mestre pode criar combates.",
        )

    combate = Combate(
        campanha_id=campanha_id,
        nome=dados.nome,
        status="ATIVO",
        rodada_atual=1,
        ordem_turno_atual=1,
    )

    db.add(combate)
    db.commit()
    db.refresh(combate)

    return combate

@router.post(
    "/{campanha_id}/combates/{combate_id}/personagens",
    response_model=CombateParticipanteResponse,
    status_code=status.HTTP_201_CREATED,
)
def adicionar_personagem_combate(
    campanha_id: int,
    combate_id: int,
    dados: CombatePersonagemAdicionar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    combate = buscar_combate_do_mestre(
        campanha_id,
        combate_id,
        usuario,
        db,
    )

    # Verifica se o personagem foi escolhido por um jogador
    # que participa desta campanha.
    associacao = db.scalar(
        select(CampanhaUsuario).where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.papel == "JOGADOR",
            CampanhaUsuario.personagem_id == dados.personagem_id,
        )
    )

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado na campanha.",
        )

    personagem = db.get(Personagem, dados.personagem_id)

    # Verifica se o personagem já está neste combate.
    participante_existente = db.scalar(
        select(CombateParticipante).where(
            CombateParticipante.combate_id == combate.id,
            CombateParticipante.personagem_id == personagem.id,
        )
    )

    if participante_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este personagem já participa do combate.",
        )

    # Define a próxima posição disponível.
    ultima_ordem = db.scalar(
        select(func.max(CombateParticipante.ordem_turno)).where(
            CombateParticipante.combate_id == combate.id,
        )
    )

    proxima_ordem = (ultima_ordem or 0) + 1

    participante = CombateParticipante(
        combate_id=combate.id,
        personagem_id=personagem.id,
        criatura_id=None,
        pv_maximo=personagem.pv_maximo,
        pv_atual=personagem.pv_atual,
        iniciativa=dados.iniciativa,
        ordem_turno=proxima_ordem,
    )

    try:
        db.add(participante)
        db.commit()
        db.refresh(participante)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível adicionar o personagem ao combate.",
        )

    return participante

@router.post(
    "/{campanha_id}/combates/{combate_id}/criaturas",
    response_model=CombateParticipanteResponse,
    status_code=status.HTTP_201_CREATED,
)
def adicionar_criatura_combate(
    campanha_id: int,
    combate_id: int,
    dados: CombateCriaturaAdicionar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    combate = buscar_combate_do_mestre(
        campanha_id,
        combate_id,
        usuario,
        db,
    )

    # Busca uma criatura cadastrada pelo Mestre.
    criatura = db.scalar(
        select(Criatura).where(
            Criatura.id == dados.criatura_id,
            Criatura.usuario_id == usuario.id,
        )
    )

    if criatura is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criatura não encontrada.",
        )

    # Verifica se a criatura já está neste combate.
    participante_existente = db.scalar(
        select(CombateParticipante).where(
            CombateParticipante.combate_id == combate.id,
            CombateParticipante.criatura_id == criatura.id,
        )
    )

    if participante_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta criatura já participa do combate.",
        )

    ultima_ordem = db.scalar(
        select(func.max(CombateParticipante.ordem_turno)).where(
            CombateParticipante.combate_id == combate.id,
        )
    )

    proxima_ordem = (ultima_ordem or 0) + 1

    participante = CombateParticipante(
        combate_id=combate.id,
        personagem_id=None,
        criatura_id=criatura.id,
        pv_maximo=criatura.pv_maximo,
        pv_atual=criatura.pv_maximo,
        iniciativa=dados.iniciativa,
        ordem_turno=proxima_ordem,
    )

    try:
        db.add(participante)
        db.commit()
        db.refresh(participante)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível adicionar a criatura ao combate.",
        )

    return participante

@router.get(
    "/{campanha_id}/combates/{combate_id}/participantes",
    response_model=list[CombateParticipanteListResponse],
)
def listar_participantes_combate(
    campanha_id: int,
    combate_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    # Verifica se o usuário participa da campanha.
    associacao = db.scalar(
        select(CampanhaUsuario).where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    # Verifica se o combate pertence à campanha.
    combate = db.scalar(
        select(Combate).where(
            Combate.id == combate_id,
            Combate.campanha_id == campanha_id,
        )
    )

    if combate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combate não encontrado.",
        )

    # Busca participantes e seus nomes.
    consulta = (
        select(
            CombateParticipante,
            func.coalesce(
                Personagem.nome,
                Criatura.nome,
            ).label("nome_participante"),
        )
        .outerjoin(
            Personagem,
            Personagem.id == CombateParticipante.personagem_id,
        )
        .outerjoin(
            Criatura,
            Criatura.id == CombateParticipante.criatura_id,
        )
        .where(
            CombateParticipante.combate_id == combate.id,
        )
        .order_by(
            CombateParticipante.iniciativa.desc(),
            CombateParticipante.ordem_turno,
        )
    )

    resultados = db.execute(consulta).all()

    return [
        CombateParticipanteListResponse(
            id=participante.id,
            combate_id=participante.combate_id,
            personagem_id=participante.personagem_id,
            criatura_id=participante.criatura_id,
            nome_participante=nome_participante,
            pv_maximo=participante.pv_maximo,
            pv_atual=participante.pv_atual,
            iniciativa=participante.iniciativa,
            ordem_turno=participante.ordem_turno,
        )
        for participante, nome_participante in resultados
    ]

@router.put(
    "/{campanha_id}/combates/{combate_id}/participantes/{participante_id}",
    response_model=CombateParticipanteResponse,
)
def atualizar_participante_combate(
    campanha_id: int,
    combate_id: int,
    participante_id: int,
    dados: CombateParticipanteUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    # Verifica se o usuário é o Mestre e se o combate está ativo.
    combate = buscar_combate_do_mestre(
        campanha_id,
        combate_id,
        usuario,
        db,
    )

    # Busca o participante dentro do combate.
    participante = db.scalar(
        select(CombateParticipante).where(
            CombateParticipante.id == participante_id,
            CombateParticipante.combate_id == combate.id,
        )
    )

    if participante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado no combate.",
        )

    # Impede que os PV atuais ultrapassem os PV máximos.
    if dados.pv_atual > participante.pv_maximo:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Os PV atuais não podem ser maiores que os PV máximos.",
        )

    # Atualiza os dados do participante.
    participante.pv_atual = dados.pv_atual
    participante.iniciativa = dados.iniciativa

    db.commit()
    db.refresh(participante)

    return participante