package ar.edu.unrc.is1.modelo.agente;

import ar.edu.unrc.is1.modelo.autor.Autor;

public abstract class AgenteIA extends Autor {

  private String id;
  private String nombre;
  private boolean activo;

  public AgenteIA(String id, String nombre, boolean activo) {
    super(id);
    this.nombre = nombre;
    this.activo = activo;
  }

  @Override
  public String obtenerNombre() {
    return this.nombre;
  }

  public boolean isActiv0() {
    return this.activo;
  }

  public void setActivo(boolean activo) {
    this.activo = activo;
  }
}
