# ckanext-dge-dataservice

Esta extensión proporciona un mecanismo para almacenar y gestionar entidades de tipo *dataservice* o servicios de datos, ver [DCAT-AP-ES/#DataService](https://datosgobes.github.io/DCAT-AP-ES/#DataService).

> [!TIP]
> Guía base y contexto del proyecto: https://github.com/datosgobes/datos.gob.es

## Descripción

En términos de funcionalidades de CKAN, esta extensión aporta:

- Personalizaciones específicas del portal [datos.gob.es](https://datos.gob.es).
- Plantillas, recursos estáticos y *helpers* asociados.

## Requisitos

### Compatibilidad

Compatibilidad con versiones de CKAN:

| Versión de CKAN | ¿Compatible?                 |
|-----------------|------------------------------|
| 2.8             | ❌ No (requiere Python 3+)    |
| 2.9             | ✅ Sí                          |
| 2.10            | ❓ Desconocido                |
| 2.11            | ❓ Desconocido                |

### Dependencias

- Una instancia de CKAN.
- La extensión [`ckanext-dge-scheming`](https://github.com/datosgobes/ckanext-dge-scheming) es necesaria para que esta extensión funcione.

## Instalación

Instalación en modo desarrollo:

```sh
pip install -e .
```

## Configuración

Activa el plugin en tu configuración de CKAN (por ejemplo, `development.ini`):

```ini
ckan.plugins = … dge-dataservice
```

### Plugins

- `dge-dataservice`


## Tests

Para ejecutar la suite de tests:

```sh
pytest --ckan-ini=test.ini ckanext/dge/tests
```

## Licencia

Este proyecto se distribuye bajo licencia **GNU Affero General Public License (AGPL) v3.0 o posterior**. Consulta el fichero [`LICENSE`](LICENSE).
