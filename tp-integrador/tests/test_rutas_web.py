from src.models.agente_ia import AgenteIA
from src.models.categoria import Categoria
from src.models.pregunta import Pregunta


def test_index_vacio(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Preguntas recientes" in response.data


def test_index_con_preguntas(client, session):
    cat = Categoria(nombre="Matemática")
    autor = AgenteIA(id="1", nombre="Profesor")
    session.add_all([cat, autor])
    session.commit()

    p = Pregunta(titulo="¿Qué es un espacio de Hilbert?", cuerpo="Definición formal", categoria=cat, autor=autor)
    session.add(p)
    session.commit()

    response = client.get("/")
    assert response.status_code == 200
    assert "¿Qué es un espacio de Hilbert?" in response.get_data(as_text=True)


def test_nueva_pregunta_get(client, session):
    cat = Categoria(nombre="Física")
    session.add(cat)
    session.commit()

    response = client.get("/preguntas/nueva")
    assert response.status_code == 200
    assert "Física" in response.get_data(as_text=True)


def test_nueva_pregunta_post_creacion_y_respuesta_auto(client, session):
    cat = Categoria(nombre="Sistemas Operativos")
    autor_def = AgenteIA(id="1", nombre="Usuario Default")
    session.add_all([cat, autor_def])
    session.commit()

    response = client.post(
        "/preguntas/nueva",
        data={
            "titulo": "¿Cómo funciona la paginación?",
            "cuerpo": "Memoria virtual y TLB",
            "categoria_id": str(cat.id),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    contenido = response.get_data(as_text=True)
    assert "¿Cómo funciona la paginación?" in contenido
    assert "Memoria virtual y TLB" in contenido
    # Verifica que se generó la respuesta automática por EstrategiaLocal
    assert "Respuesta generada para:" in contenido


def test_detalle_pregunta_get(client, session):
    cat = Categoria(nombre="Redes")
    autor = AgenteIA(id="1", nombre="RedBot")
    session.add_all([cat, autor])
    session.commit()

    p = Pregunta(titulo="Duda sobre DNS", cuerpo="Explicar registros A y CNAME", categoria=cat, autor=autor)
    session.add(p)
    session.commit()

    # GET exitoso
    response = client.get(f"/preguntas/{p.id}")
    assert response.status_code == 200
    assert "Duda sobre DNS" in response.get_data(as_text=True)

    # 404 para ID inexistente
    response_404 = client.get("/preguntas/99999")
    assert response_404.status_code == 404


def test_detalle_pregunta_post_respuesta_manual(client, session):
    cat = Categoria(nombre="Bases de Datos")
    autor = AgenteIA(id="1", nombre="DBBot")
    session.add_all([cat, autor])
    session.commit()

    p = Pregunta(titulo="Normalización 3FN", cuerpo="Duda con transitividad", categoria=cat, autor=autor)
    session.add(p)
    session.commit()

    response = client.post(
        f"/preguntas/{p.id}",
        data={"cuerpo": "Para estar en 3FN no debe haber dependencias transitivas."},
        follow_redirects=True,
    )
    assert response.status_code == 200
    contenido = response.get_data(as_text=True)
    assert "dependencias transitivas" in contenido
    assert len(p.respuestas) == 1
