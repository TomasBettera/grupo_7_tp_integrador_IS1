import pytest
from src.fabricas.fabrica_autor import FabricaAutor
from src.fabricas.fabrica_usuario import FabricaUsuario
from src.models.autor import Autor, TUsuario
from src.models.agente_ia import AgenteIA
from src.models.usuario import Usuario


def test_creacion_directa_usuario(session):
    usuario = Usuario(
        email="tomas@gmail.com",
        password="passwordSegura123",
        tipo=TUsuario.GENERAL,
    )
    session.add(usuario)
    session.commit()

    assert usuario.id is not None
    assert usuario.obtener_nombre() == "tomas@gmail.com"
    assert usuario.obtenerNombre() == "tomas@gmail.com"
    assert usuario.tipo == TUsuario.GENERAL
    assert isinstance(usuario, Autor)
    assert usuario.autenticar("passwordSegura123") is True
    assert usuario.autenticar("passwordIncorrecta") is False
    assert usuario.autenticar(None) is False
    assert usuario.autenticar(12345) is False


def test_validaciones_modelo_usuario():
    # Email inválido
    with pytest.raises(ValueError, match="El email es obligatorio"):
        Usuario(email="", password="password123", tipo=TUsuario.GENERAL)

    with pytest.raises(ValueError, match="El email es obligatorio"):
        Usuario(email="   ", password="password123", tipo=TUsuario.GENERAL)

    with pytest.raises(ValueError, match="El email es obligatorio"):
        Usuario(email=123, password="password123", tipo=TUsuario.GENERAL)

    # Contraseña inválida
    with pytest.raises(ValueError, match="La contraseña es obligatoria"):
        Usuario(email="user@test.com", password="", tipo=TUsuario.GENERAL)

    with pytest.raises(ValueError, match="La contraseña es obligatoria"):
        Usuario(email="user@test.com", password=None, tipo=TUsuario.GENERAL)

    # Tipo inválido
    with pytest.raises(ValueError, match="El rol debe ser un valor de TUsuario"):
        Usuario(email="user@test.com", password="password123", tipo="admin_invalido")

    # Normalización de email (lowercase y strip)
    u = Usuario(email="  MiCorreo@Dominio.COM  ", password="pass", tipo=TUsuario.ADMIN)
    assert u.email == "micorreo@dominio.com"


def test_fabrica_usuario(session):
    fabrica: FabricaAutor = FabricaUsuario(
        email="nacho@gmail.com",
        password="secretpassword",
        tipo=TUsuario.ADMIN,
    )
    usuario = fabrica.crear_autor()
    session.add(usuario)
    session.commit()

    assert usuario.id is not None
    assert usuario.email == "nacho@gmail.com"
    assert usuario.tipo == TUsuario.ADMIN
    assert isinstance(usuario, Usuario)
    assert isinstance(usuario, Autor)
    assert usuario.autenticar("secretpassword") is True


def test_fabrica_usuario_override_y_camelcase(session):
    fabrica = FabricaUsuario(email="default@test.com", password="pass_default")

    # Override mediante kwargs y llamada a método camelCase del diagrama UML
    usuario = fabrica.crearAutor(
        email="joaquin@gmail.com",
        password="nueva_password",
        tipo=TUsuario.GENERAL,
    )
    session.add(usuario)
    session.commit()

    assert usuario.email == "joaquin@gmail.com"
    assert usuario.tipo == TUsuario.GENERAL
    assert usuario.autenticar("nueva_password") is True
    assert usuario.autenticar("pass_default") is False


def test_polimorfismo_autores_con_usuarios_y_agentes(session):
    fab_usuario = FabricaUsuario(email="maxi@gmail.com", password="passwordMaxi")
    usuario = fab_usuario.crear_autor()

    agente = AgenteIA(nombre="Bot Docente", activo=True)

    session.add_all([usuario, agente])
    session.commit()

    # Consulta polimórfica en la raíz de la jerarquía Autor
    autores = Autor.query.all()
    assert len(autores) == 2

    nombres = [a.obtener_nombre() for a in autores]
    assert "maxi@gmail.com" in nombres
    assert "Bot Docente" in nombres

    nombres_camel = [a.obtenerNombre() for a in autores]
    assert "maxi@gmail.com" in nombres_camel
    assert "Bot Docente" in nombres_camel

    # Verificación de identidades polimórficas (columna discriminadora en tabla autores)
    identidades = [a.tipo_autor for a in autores]
    assert "usuario" in identidades
    assert "agente_ia" in identidades

    # Verificación de subclases concretas instanciadas polimórficamente
    usuarios = [a for a in autores if isinstance(a, Usuario)]
    agentes = [a for a in autores if isinstance(a, AgenteIA)]
    assert len(usuarios) == 1
    assert len(agentes) == 1
    assert usuarios[0].tipo == TUsuario.GENERAL
