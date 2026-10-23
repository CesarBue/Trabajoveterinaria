from modelos.mascota import Mascota

class MascotaControlador:
    
    @staticmethod
    def registrar_mascota(id_usuario, nombre, tipo, raza, edad, peso, observaciones):
        """Valida los datos y registra una nueva mascota vinculada al usuario."""
        errores = []
        
        # Validaciones de campos obligatorios y formatos
        if not nombre.strip():
            errores.append("El nombre es obligatorio.")
        if not tipo.strip():
            errores.append("El tipo de mascota es obligatorio.")
        if not raza.strip():
            errores.append("La raza es obligatoria.")

        try:
            edad_num = int(edad)
            if edad_num < 0:
                errores.append("La edad no puede ser negativa.")
        except ValueError:
            errores.append("La edad debe ser un número entero.")

        try:
            peso_num = float(peso)
            if peso_num <= 0:
                errores.append("El peso debe ser mayor que 0.")
        except ValueError:
            errores.append("El peso debe ser un número.")

        if errores:
            return False, errores

        # Si no hay errores, creamos la instancia del modelo y guardamos en BD
        nueva_mascota = Mascota(
            id_usuario=id_usuario,
            nombre=nombre.strip(),
            tipo=tipo.strip(),
            raza=raza.strip(),
            edad=int(edad),
            peso=float(peso),
            observaciones=observaciones.strip()
        )
        
        try:
            nueva_mascota.guardar()
            return True, f"¡{nombre} ha sido registrada correctamente!"
        except Exception as e:
            return False, [f"Error al guardar en la base de datos: {e}"]

    @staticmethod
    def listar_mascotas_usuario(id_usuario):
        """Obtiene la lista de mascotas para mostrarlas en la interfaz."""
        return Mascota.obtener_por_usuario(id_usuario)
