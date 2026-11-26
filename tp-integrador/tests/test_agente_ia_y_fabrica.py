from src.fabricas.fabrica_agente_ia import FabricaAgenteIA
from src.fabricas.fabrica_autor import FabricaAutor
from src.models.agente_ia import AgenteIA
from src.models.autor import Autor


def test_creacion_directa_agente_ia(session):
    agente = AgenteIA(nombre="GeminiBot", activo=True)
    session.add(agente)
    session.commit()

    assert agente.id is not None
    assert agente.obtener_nombre() == "GeminiBot"
    assert agente.obtenerNombre() == "GeminiBot"
    assert agente.esta_activo() is True
    assert isinstance(agente, Autor)
    assert agente.tipo == "agente_ia"


def test_fabrica_agente_ia(session):
    fabrica: FabricaAutor = FabricaAgenteIA()
    agente = fabrica.crear_autor(nombre="OpenAIBot", activo=False)
    session.add(agente)
    session.commit()

    assert agente.id is not None
    assert agente.obtener_nombre() == "OpenAIBot"
    assert agente.esta_activo() is False
    assert isinstance(agente, AgenteIA)
    assert isinstance(agente, Autor)


def test_polimorfismo_autor(session):
    fabrica = FabricaAgenteIA()
    agente1 = fabrica.crearAutor(nombre="Bot Alfa")
    agente2 = fabrica.crearAutor(nombre="Bot Beta")

    session.add_all([agente1, agente2])
    session.commit()

    # Consulta polimórfica a través de la clase base Autor
    autores = Autor.query.all()
    assert len(autores) == 2
    nombres = [a.obtener_nombre() for a in autores]
    assert "Bot Alfa" in nombres
    assert "Bot Beta" in nombres
