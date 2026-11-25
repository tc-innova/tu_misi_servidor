CREATE TABLE tenants (
    id_tenant BIGINT GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(150) NOT NULL,
    CONSTRAINT pk_tenants PRIMARY KEY (id_tenant),
    CONSTRAINT uq_tenants_nombre UNIQUE (nombre)
);

CREATE TABLE tipo_productos (
    id_tipo_producto BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT pk_tipo_productos PRIMARY KEY (id_tipo_producto),
    CONSTRAINT uq_tipo_productos_nombre UNIQUE (id_tenant, nombre),
    CONSTRAINT fk_tipo_productos_tenants FOREIGN KEY (id_tenant) REFERENCES tenants (id_tenant)
);

CREATE TABLE tipo_proveedores (
    id_tipo_proveedor BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT pk_tipo_proveedores PRIMARY KEY (id_tipo_proveedor),
    CONSTRAINT uq_tipo_proveedores_nombre UNIQUE (id_tenant, nombre),
    CONSTRAINT fk_tipo_proveedores_tenants FOREIGN KEY (id_tenant) REFERENCES tenants (id_tenant)
);

CREATE TABLE proveedores (
    id_proveedor BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    id_tipo_proveedor BIGINT NOT NULL,
    es_empresa BOOLEAN NOT NULL DEFAULT FALSE,
    nombre VARCHAR(150) NOT NULL,
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    nit VARCHAR(20),
    ci VARCHAR(20),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_proveedores PRIMARY KEY (id_proveedor),
    CONSTRAINT ck_proveedores_tipo CHECK (
        (es_empresa
            AND nit IS NOT NULL
            AND apellido_paterno IS NULL AND apellido_materno IS NULL AND ci IS NULL)
        OR
        (NOT es_empresa
            AND apellido_paterno IS NOT NULL AND (ci IS NOT NULL OR nit IS NOT NULL))
    ),
    CONSTRAINT uq_proveedores_nit UNIQUE (id_tenant, nit),
    CONSTRAINT uq_proveedores_ci UNIQUE (id_tenant, ci),
    CONSTRAINT fk_proveedores_tenants FOREIGN KEY (id_tenant) REFERENCES tenants (id_tenant),
    CONSTRAINT fk_proveedores_tipo_proveedores FOREIGN KEY (id_tipo_proveedor) REFERENCES tipo_proveedores (id_tipo_proveedor)
);

CREATE TABLE clientes (
    id_cliente BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    es_empresa BOOLEAN NOT NULL DEFAULT FALSE,
    nombre VARCHAR(150) NOT NULL,
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    ci VARCHAR(20),
    nit VARCHAR(20),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_clientes PRIMARY KEY (id_cliente),
    CONSTRAINT ck_clientes_tipo CHECK (
        (es_empresa
            AND nit IS NOT NULL
            AND apellido_paterno IS NULL AND apellido_materno IS NULL AND ci IS NULL)
        OR
        (NOT es_empresa
            AND apellido_paterno IS NOT NULL AND (ci IS NOT NULL OR nit IS NOT NULL))
    ),
    CONSTRAINT uq_clientes_ci UNIQUE (id_tenant, ci),
    CONSTRAINT uq_clientes_nit UNIQUE (id_tenant, nit),
    CONSTRAINT fk_clientes_tenants FOREIGN KEY (id_tenant) REFERENCES tenants (id_tenant)
);

CREATE TABLE estados_venta (
    id_estado_venta BIGINT GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(30) NOT NULL,
    CONSTRAINT pk_estados_venta PRIMARY KEY (id_estado_venta),
    CONSTRAINT uq_estados_venta_nombre UNIQUE (nombre)
);

CREATE TABLE estados_compra (
    id_estado_compra BIGINT GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(30) NOT NULL,
    CONSTRAINT pk_estados_compra PRIMARY KEY (id_estado_compra),
    CONSTRAINT uq_estados_compra_nombre UNIQUE (nombre)
);

CREATE TABLE formas_pago (
    id_forma_pago BIGINT GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(30) NOT NULL,
    CONSTRAINT pk_formas_pago PRIMARY KEY (id_forma_pago),
    CONSTRAINT uq_formas_pago_nombre UNIQUE (nombre)
);

CREATE TABLE roles (
    id_rol BIGINT GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(50) NOT NULL,
    CONSTRAINT pk_roles PRIMARY KEY (id_rol),
    CONSTRAINT uq_roles_nombre UNIQUE (nombre)
);

CREATE TABLE administradores (
    id_administrador BIGINT GENERATED ALWAYS AS IDENTITY,
    nombres VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    fecha_nacimiento DATE NOT NULL,
    sexo BOOLEAN NOT NULL,
    ci VARCHAR(20) NOT NULL,
    usuario VARCHAR(50) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_administradores PRIMARY KEY (id_administrador),
    CONSTRAINT uq_administradores_ci UNIQUE (ci),
    CONSTRAINT uq_administradores_usuario UNIQUE (usuario)
);

CREATE TABLE usuarios (
    id_usuario BIGINT GENERATED ALWAYS AS IDENTITY,
    nombres VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    fecha_nacimiento DATE NOT NULL,
    sexo BOOLEAN NOT NULL,
    ci VARCHAR(20) NOT NULL,
    usuario VARCHAR(50) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuarios_ci UNIQUE (ci),
    CONSTRAINT uq_usuarios_usuario UNIQUE (usuario)
);

CREATE TABLE usuarios_tenants (
    id_usuario BIGINT NOT NULL,
    id_tenant BIGINT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_usuarios_tenants PRIMARY KEY (id_usuario, id_tenant),
    CONSTRAINT fk_usuarios_tenants_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
    CONSTRAINT fk_usuarios_tenants_tenants FOREIGN KEY (id_tenant) REFERENCES tenants (id_tenant)
);

CREATE TABLE usuarios_roles (
    id_usuario BIGINT NOT NULL,
    id_tenant BIGINT NOT NULL,
    id_rol BIGINT NOT NULL,
    CONSTRAINT pk_usuarios_roles PRIMARY KEY (id_usuario, id_tenant, id_rol),
    CONSTRAINT fk_usuarios_roles_usuarios_tenants FOREIGN KEY (id_usuario, id_tenant) REFERENCES usuarios_tenants (id_usuario, id_tenant),
    CONSTRAINT fk_usuarios_roles_roles FOREIGN KEY (id_rol) REFERENCES roles (id_rol)
);

CREATE TABLE productos (
    id_producto BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    id_tipo_producto BIGINT NOT NULL,
    codigo_barras VARCHAR(50),
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(12, 2) NOT NULL,
    cantidad INTEGER NOT NULL,
    cantidad_minima INTEGER NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_productos PRIMARY KEY (id_producto),
    CONSTRAINT uq_productos_codigo_barras UNIQUE (id_tenant, codigo_barras),
    CONSTRAINT ck_productos_cantidad CHECK (cantidad >= 0),
    CONSTRAINT ck_productos_cantidad_minima CHECK (cantidad_minima >= 0),
    CONSTRAINT fk_productos_tenants FOREIGN KEY (id_tenant) REFERENCES tenants (id_tenant),
    CONSTRAINT fk_productos_tipo_productos FOREIGN KEY (id_tipo_producto) REFERENCES tipo_productos (id_tipo_producto)
);

CREATE TABLE fotos_productos (
    id_producto BIGINT NOT NULL,
    numero INTEGER NOT NULL,
    foto BYTEA NOT NULL,
    CONSTRAINT pk_fotos_productos PRIMARY KEY (id_producto, numero),
    CONSTRAINT ck_fotos_productos_numero CHECK (numero > 0),
    CONSTRAINT fk_fotos_productos_productos FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
);

CREATE TABLE celulares_proveedores (
    id_proveedor BIGINT NOT NULL,
    codigo_pais VARCHAR(5) NOT NULL,
    numero VARCHAR(15) NOT NULL,
    CONSTRAINT pk_celulares_proveedores PRIMARY KEY (id_proveedor, codigo_pais, numero),
    CONSTRAINT fk_celulares_proveedores_proveedores FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor)
);

CREATE TABLE celulares_clientes (
    id_cliente BIGINT NOT NULL,
    codigo_pais VARCHAR(5) NOT NULL,
    numero VARCHAR(15) NOT NULL,
    CONSTRAINT pk_celulares_clientes PRIMARY KEY (id_cliente, codigo_pais, numero),
    CONSTRAINT fk_celulares_clientes_clientes FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
);

CREATE TABLE celulares_usuarios (
    id_usuario BIGINT NOT NULL,
    codigo_pais VARCHAR(5) NOT NULL,
    numero VARCHAR(15) NOT NULL,
    CONSTRAINT pk_celulares_usuarios PRIMARY KEY (id_usuario, codigo_pais, numero),
    CONSTRAINT fk_celulares_usuarios_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
);

CREATE TABLE correos_proveedores (
    id_proveedor BIGINT NOT NULL,
    correo VARCHAR(150) NOT NULL,
    CONSTRAINT pk_correos_proveedores PRIMARY KEY (id_proveedor, correo),
    CONSTRAINT fk_correos_proveedores_proveedores FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor)
);

CREATE TABLE correos_clientes (
    id_cliente BIGINT NOT NULL,
    correo VARCHAR(150) NOT NULL,
    CONSTRAINT pk_correos_clientes PRIMARY KEY (id_cliente, correo),
    CONSTRAINT fk_correos_clientes_clientes FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
);

CREATE TABLE correos_usuarios (
    id_usuario BIGINT NOT NULL,
    correo VARCHAR(150) NOT NULL,
    CONSTRAINT pk_correos_usuarios PRIMARY KEY (id_usuario, correo),
    CONSTRAINT uq_correos_usuarios_correo UNIQUE (correo),
    CONSTRAINT fk_correos_usuarios_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
);

CREATE TABLE ventas (
    id_venta BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    id_cliente BIGINT,
    id_usuario BIGINT NOT NULL,
    id_estado_venta BIGINT NOT NULL,
    id_forma_pago BIGINT NOT NULL,
    fecha_venta DATE NOT NULL,
    hora_venta TIME NOT NULL,
    CONSTRAINT pk_ventas PRIMARY KEY (id_venta),
    CONSTRAINT fk_ventas_clientes FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT fk_ventas_usuarios_tenants FOREIGN KEY (id_usuario, id_tenant) REFERENCES usuarios_tenants (id_usuario, id_tenant),
    CONSTRAINT fk_ventas_estados_venta FOREIGN KEY (id_estado_venta) REFERENCES estados_venta (id_estado_venta),
    CONSTRAINT fk_ventas_formas_pago FOREIGN KEY (id_forma_pago) REFERENCES formas_pago (id_forma_pago)
);

CREATE TABLE compras (
    id_compra BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    id_proveedor BIGINT,
    id_usuario BIGINT NOT NULL,
    id_estado_compra BIGINT NOT NULL,
    id_forma_pago BIGINT NOT NULL,
    fecha_compra DATE NOT NULL,
    hora_compra TIME NOT NULL,
    CONSTRAINT pk_compras PRIMARY KEY (id_compra),
    CONSTRAINT fk_compras_proveedores FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor),
    CONSTRAINT fk_compras_usuarios_tenants FOREIGN KEY (id_usuario, id_tenant) REFERENCES usuarios_tenants (id_usuario, id_tenant),
    CONSTRAINT fk_compras_estados_compra FOREIGN KEY (id_estado_compra) REFERENCES estados_compra (id_estado_compra),
    CONSTRAINT fk_compras_formas_pago FOREIGN KEY (id_forma_pago) REFERENCES formas_pago (id_forma_pago)
);

CREATE TABLE detalle_ventas (
    id_venta BIGINT NOT NULL,
    id_producto BIGINT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario NUMERIC(12, 2) NOT NULL,
    CONSTRAINT pk_detalle_ventas PRIMARY KEY (id_venta, id_producto),
    CONSTRAINT fk_detalle_ventas_ventas FOREIGN KEY (id_venta) REFERENCES ventas (id_venta),
    CONSTRAINT fk_detalle_ventas_productos FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
);

CREATE TABLE detalle_compras (
    id_compra BIGINT NOT NULL,
    id_producto BIGINT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario NUMERIC(12, 2) NOT NULL,
    CONSTRAINT pk_detalle_compras PRIMARY KEY (id_compra, id_producto),
    CONSTRAINT fk_detalle_compras_compras FOREIGN KEY (id_compra) REFERENCES compras (id_compra),
    CONSTRAINT fk_detalle_compras_productos FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
);

CREATE TABLE tipo_acciones (
    id_tipo_accion BIGINT GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(30) NOT NULL,
    CONSTRAINT pk_tipo_acciones PRIMARY KEY (id_tipo_accion),
    CONSTRAINT uq_tipo_acciones_nombre UNIQUE (nombre)
);

CREATE TABLE auditorias (
    id_auditoria BIGINT GENERATED ALWAYS AS IDENTITY,
    id_tenant BIGINT NOT NULL,
    id_usuario BIGINT,
    tabla VARCHAR(50) NOT NULL,
    id_registro VARCHAR(100) NOT NULL,
    id_tipo_accion BIGINT NOT NULL,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    CONSTRAINT pk_auditorias PRIMARY KEY (id_auditoria),
    CONSTRAINT fk_auditorias_tenants FOREIGN KEY (id_tenant) REFERENCES tenants (id_tenant),
    CONSTRAINT fk_auditorias_usuarios_tenants FOREIGN KEY (id_usuario, id_tenant) REFERENCES usuarios_tenants (id_usuario, id_tenant),
    CONSTRAINT fk_auditorias_tipo_acciones FOREIGN KEY (id_tipo_accion) REFERENCES tipo_acciones (id_tipo_accion)
);

CREATE INDEX idx_ventas_tenant_fecha ON ventas (id_tenant, fecha_venta);
CREATE INDEX idx_ventas_cliente ON ventas (id_cliente);
CREATE INDEX idx_ventas_usuario ON ventas (id_usuario);
CREATE INDEX idx_compras_tenant_fecha ON compras (id_tenant, fecha_compra);
CREATE INDEX idx_compras_proveedor ON compras (id_proveedor);
CREATE INDEX idx_compras_usuario ON compras (id_usuario);
CREATE INDEX idx_detalle_ventas_producto ON detalle_ventas (id_producto);
CREATE INDEX idx_detalle_compras_producto ON detalle_compras (id_producto);
CREATE INDEX idx_productos_tipo_producto ON productos (id_tipo_producto);
CREATE INDEX idx_productos_tenant ON productos(id_tenant);
CREATE INDEX idx_productos_activo ON productos(activo);
CREATE INDEX idx_productos_tenant_activo ON productos(id_tenant, activo);
CREATE INDEX idx_usuarios_roles_rol ON usuarios_roles (id_rol);
CREATE INDEX idx_usuarios_tenants_tenant ON usuarios_tenants (id_tenant);
CREATE INDEX idx_auditorias_tenant_fecha ON auditorias (id_tenant, fecha);
CREATE INDEX idx_auditorias_tabla_registro ON auditorias (tabla, id_registro);

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_productos_nombre_trgm ON productos USING GIN (nombre gin_trgm_ops);
CREATE INDEX idx_clientes_nombre_trgm ON clientes USING GIN (nombre gin_trgm_ops);
CREATE INDEX idx_clientes_apellido_paterno_trgm ON clientes USING GIN (apellido_paterno gin_trgm_ops);
CREATE INDEX idx_clientes_apellido_materno_trgm ON clientes USING GIN (apellido_materno gin_trgm_ops);
CREATE INDEX idx_proveedores_nombre_trgm ON proveedores USING GIN (nombre gin_trgm_ops);
CREATE INDEX idx_proveedores_apellido_paterno_trgm ON proveedores USING GIN (apellido_paterno gin_trgm_ops);
CREATE INDEX idx_proveedores_apellido_materno_trgm ON proveedores USING GIN (apellido_materno gin_trgm_ops);

INSERT INTO roles (nombre) VALUES ('propietario');

INSERT INTO estados_venta (nombre) VALUES ('activa'), ('anulada');

INSERT INTO estados_compra (nombre) VALUES ('activa'), ('anulada');

INSERT INTO formas_pago (nombre) VALUES ('efectivo'), ('transferencia'), ('qr'), ('tarjeta');

INSERT INTO tipo_acciones (nombre) VALUES ('crear'), ('modificar'), ('eliminar');